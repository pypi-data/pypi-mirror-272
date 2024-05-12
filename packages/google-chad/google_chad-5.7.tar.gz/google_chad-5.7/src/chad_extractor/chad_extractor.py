#!/usr/bin/env python3

import argparse, asyncio, collections,  colorama, concurrent.futures, copy, datetime, json, os, random, regex as re, signal, subprocess, sys, termcolor, threading, time, urllib.parse
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
# from playwright._impl._api_types import Error as PlaywrightError # playwright<1.40.0
from playwright._impl._errors import Error as PlaywrightError
from nagooglesearch import nagooglesearch

colorama.init(autoreset = True)

# ----------------------------------------

class Stopwatch:

	def __init__(self):
		self.__start = datetime.datetime.now()

	def stop(self):
		self.__end = datetime.datetime.now()
		print(("Script has finished in {0}").format(self.__end - self.__start))

	def get_start(self):
		return self.__start

stopwatch = Stopwatch()

# ----------------------------------------

def check_directory_files(directory): # non-recursive
	tmp = []
	for file in os.listdir(directory):
		file = os.path.join(directory, file)
		if os.path.isfile(file) and os.access(file, os.R_OK) and os.stat(file).st_size > 0:
			tmp.append(file)
	return tmp

def unique(sequence, sort = False):
	seen = set()
	array = [x for x in sequence if not (x in seen or seen.add(x))]
	if sort and array:
		array = sorted(array, key = str.casefold)
	return array

encoding = "ISO-8859-1"

def read_file(file, sort = False, array = True):
	return __read_file_array(file, sort) if array else __read_file_text(file)

def __read_file_array(file, sort = False):
	tmp = []
	with open(file, "r", encoding = encoding) as stream:
		for line in stream:
			line = line.strip()
			if line:
				tmp.append(line)
	return unique(tmp, sort)

def __read_file_text(file):
	return open(file, "r", encoding = encoding).read()

def write_file(data, out):
	confirm = "yes"
	if os.path.isfile(out):
		print(("'{0}' already exists").format(out))
		confirm = input("Overwrite the output file (yes): ")
	if confirm.lower() == "yes":
		try:
			open(out, "w").write(data)
			print(("Results have been saved to '{0}'").format(out))
		except FileNotFoundError:
			print(("Cannot save results to '{0}'").format(out))

def write_file_silent(data, out):
	try:
		open(out, "w").write(data)
	except FileNotFoundError:
		pass

def jload_file(file):
	tmp = []
	try:
		tmp = json.loads(read_file(file, array = False))
	except json.decoder.JSONDecodeError:
		pass
	return tmp

def jdump(data):
	return json.dumps(data, indent = 4, ensure_ascii = False) if data else ""

def get_timestamp(text):
	print(("{0} - {1}").format(datetime.datetime.now().strftime("%H:%M:%S"), text))

# ----------------------------------------

def select(obj, key, sort = False):
	tmp = []
	for entry in obj:
		tmp.append(entry[key])
	return unique(tmp, sort)

def select_array(obj, key, sort = False):
	tmp = []
	for entry in obj:
		tmp.extend(entry[key])
	return unique(tmp, sort)

def sort_by(obj, key):
	return sorted(obj, key = lambda entry: entry[key].casefold())

def group_by_url(obj, sort = False):
	grouped = collections.defaultdict(lambda: {"files": []})
	for entry in obj:
		url = entry["url"]
		grouped[url]["url"] = entry["url"]
		if "key" in entry:
			grouped[url]["key"] = entry["key"]
		grouped[url]["files"].append(entry["file"])
	tmp = []
	for entry in list(grouped.values()):
		entry["files"] = unique(entry["files"], sort)
		tmp.append(entry)
	return tmp

def delete(obj, key):
	tmp = []
	for entry in copy.deepcopy(obj):
		entry.pop(key, None)
		tmp.append(entry)
	return tmp

def select_results_array(obj, sort = False):
	tmp = []
	for entry in obj:
		for key in entry["results"]:
			tmp.extend(entry["results"][key])
	return unique(tmp, sort)

def select_by_file(obj, file):
	tmp = []
	for entry in obj:
		if file in entry["file"]:
			tmp.append(entry)
	return tmp

def select_url_by_file(obj, file, sort = False):
	tmp = []
	for entry in obj:
		if file in entry["files"]:
			tmp.append(entry["url"])
	return tmp

def select_by_file_delete_files(obj, file, sort = False):
	tmp = []
	for entry in copy.deepcopy(obj):
		if file in entry["files"]:
			entry.pop("files", None)
			tmp.append(entry)
	return tmp

def jquery(obj, query, value = None, sort = False):
	if query == "select_url":
		return select(obj, "url", sort)
	elif query == "select_urls":
		return select_array(obj, "urls", sort)
	elif query == "sort_by_url":
		return sort_by(obj, "url")
	elif query == "group_by_url":
		return group_by_url(obj, sort)
	elif query == "select_file":
		return select(obj, "file", sort)
	elif query == "select_files":
		return select_array(obj, "files", sort)
	elif query == "sort_by_file":
		return sort_by(obj, "file")
	elif query == "delete_files":
		return delete(obj, "files")
	elif query == "select_results":
		return select_results_array(obj, sort)
	elif query == "select_by_file":
		return select_by_file(obj, value)
	elif query == "select_by_file_delete_files":
		return select_by_file_delete_files(obj, value, sort)
	elif query == "select_url_by_file":
		return select_url_by_file(obj, value, sort)

# ----------------------------------------

class ChadExtractor:

	def __init__(self, template, results, excludes, threads, retries, wait, user_agents, proxy, out, extension, verbose, debug):
		self.__template        = template
		self.__results         = results
		self.__excludes        = excludes
		self.__threads         = threads
		self.__retries         = retries
		self.__wait            = wait
		self.__start           = 4 # delay between starting each headless browser
		self.__user_agents     = user_agents if user_agents else nagooglesearch.get_all_user_agents()
		self.__user_agents_len = len(self.__user_agents)
		self.__proxy           = {"server": proxy} if proxy else None
		self.__out             = out
		self.__extension       = extension
		self.__verbose         = verbose # verbose report extension
		self.__debug           = debug
		self.__debug_lock      = threading.Lock()
		# --------------------------------
		self.__keys            = {
			"extract": True,
			"active" : None,
			"data"   : {
				"extract" : {
					"template": "extract",
					"success" : "extracted",
					"failure" : "failed_extraction",
					"error"   : "extraction",
					"prepend" : "extract_prepend",
					"append"  : "extract_append"
				},
				"validate": {
					"template": "validate",
					"success" : "validated",
					"failure" : "failed_validation",
					"error"   : "validation",
					"prepend" : "validate_prepend",
					"append"  : "validate_append"
				}
			}
		}
		self.__keys["active"]  = self.__keys["data"]["extract"]
		# --------------------------------
		self.__data            = {
			self.__keys["data"]["extract" ]["success"]: [],
			self.__keys["data"]["extract" ]["failure"]: [],
			self.__keys["data"]["validate"]["success"]: [],
			self.__keys["data"]["validate"]["failure"]: []
		}
		self.__data_lock       = threading.Lock()
		# --------------------------------
		self.__flags           = re.MULTILINE | re.IGNORECASE
		self.__close           = False

	def set_validate(self):
		self.__keys["extract"] = False
		self.__keys["active" ] = self.__keys["data"]["validate"]

	def __extend_data(self, success, failure):
		with self.__data_lock:
			self.__data[self.__keys["active"]["success"]].extend(success)
			self.__data[self.__keys["active"]["failure"]].extend(failure)

	def parse_template(self):
		tmp = {}
		for key in self.__template:
			if self.__keys["active"]["template"] in self.__template[key]:
				tmp[key] = self.__template[key]
		self.__template = tmp
		return bool(self.__template)

	def parse_input(self, plaintext = False):
		tmp = []
		if self.__keys["extract"]:
			if not plaintext:
				for file in self.__results:
					for url in jquery(jload_file(file), "select_urls"):
						tmp.append(self.__input(url, None, file))
			else:
				for file in self.__results:
					results = self.__parse_response(None, read_file(file, array = False)) # plaintext files are treated like server responses
					if results:
						self.__data[self.__keys["data"]["extract"]["success"]].append(self.__output_plaintext(file, results))
				return bool(self.__data[self.__keys["data"]["extract"]["success"]])
		else:
			if not plaintext:
				for entry in self.__data[self.__keys["data"]["extract"]["success"]]:
					for key in entry["results"]:
						if key in self.__template:
							for url in entry["results"][key]:
								for file in entry["files"]:
									tmp.append(self.__input(url, key, file))
			else:
				for entry in self.__data[self.__keys["data"]["extract"]["success"]]:
					for key in entry["results"]:
						if key in self.__template:
							for url in entry["results"][key]:
								tmp.append(self.__input(url, key, entry["file"]))
		self.__results = jquery(tmp, "group_by_url")
		return bool(self.__results)

	def __input(self, url, key, file):
		return {"url": url, "key": key, "file": file}

	def __output(self, url, results, files):
		return {"url": url, "results": results, "files": files}

	def __output_plaintext(self, file, results):
		return {"file": file, "results": results}

	def __parse_response(self, record, response):
		tmp = {}
		try:
			if self.__keys["extract"]:
				if self.__excludes:
					for exclude in self.__excludes:
						response = re.sub(exclude, "", response, flags = self.__flags)
				for key in self.__template:
					matches = re.findall(self.__template[key][self.__keys["data"]["extract"]["template"]], response, flags = self.__flags)
					if matches:
						tmp[key] = self.__concat(key, matches)
			elif re.search(self.__template[record["key"]][self.__keys["data"]["validate"]["template"]], response, flags = self.__flags):
				tmp = True
		except (re.error, KeyError) as ex:
			self.__print_error(ex)
		return tmp

	def __concat(self, key, matches):
		prepend = ""
		if self.__keys["data"]["extract"]["prepend"] in self.__template[key]:
			prepend = self.__template[key][self.__keys["data"]["extract"]["prepend"]]
		append = ""
		if self.__keys["data"]["extract"]["append"] in self.__template[key]:
			append = self.__template[key][self.__keys["data"]["extract"]["append"]]
		if prepend or append:
			for i in range(len(matches)):
				matches[i] = ("{0}{1}{2}").format(prepend, matches[i], append)
		return unique(matches, sort = True)

	def run(self):
		signal.signal(signal.SIGINT, self.__interrupt)
		self.__close = False
		get_timestamp(("Number of URLs to {0}: {1}").format(self.__keys["active"]["template"], len(self.__results)))
		print("Press CTRL + C to exit early - results will be saved")
		random.shuffle(self.__results) # anti-bot evasion 1
		with concurrent.futures.ThreadPoolExecutor(max_workers = self.__threads) as executor:
			subprocesses = []
			for records in self.__split_results():
				if self.__close:
					break
				if subprocesses:
					time.sleep(self.__start)
				subprocesses.append(executor.submit(self.__proxy_browser_requests, records, len(subprocesses) + 1))
			concurrent.futures.wait(subprocesses)
		if not self.__keys["extract"]:
			signal.signal(signal.SIGINT, signal.SIG_DFL)
		return bool(self.__data[self.__keys["active"]["success"]])

	def __interrupt(self, signum, frame):
		self.__close = True
		self.__print_lock("Please wait for a clean exit...")

	def __split_results(self):
		if self.__threads > 1:
			k, m = divmod(len(self.__results), self.__threads)
			return list(filter(None, [self.__results[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(self.__threads)]))
		else:
			return [self.__results]

	def __proxy_browser_requests(self, records, identifier):
		if not self.__close:
			self.__print_lock(("Running browser thread #{0}").format(identifier))
			asyncio.run(self.__browser_requests(records))

	async def __browser_requests(self, records):
		success = []
		failure = []
		pw      = None
		browser = None
		context = None
		# --------------------------------
		try:
			pw      = await async_playwright().start()
			browser = await pw.chromium.launch(
				headless      = True,
				handle_sigint = False, # do not terminate the browser on 'CTRL + C'
				proxy         = self.__proxy
			)
			context = await self.__set_context(browser)
			context.set_default_timeout(30000)
			# ----------------------------
			cache_reset = 0
			cache_limit = 100
			for record in records:
				if self.__close:
					break
				# playwright issue / bug
				# reusing same context leads to large resource consumption and crash
				cache_reset += 1
				if cache_reset % cache_limit:
					cache_reset = 0
					await context.close()
					context = await self.__set_context(browser)
				# ------------------------
				entry   = self.__output(record["url"], None, record["files"])
				retries = self.__retries + 1
				while retries > 0 and not self.__close:
					await context.set_extra_http_headers(self.__get_headers()) # anti-bot evasion 2
					# --------------------
					tmp = await self.__page_get(context, record["url"])
					if tmp["error"]:
						tmp = await self.__request_get(context, record["url"])
						if tmp["error"]:
							retries = 0
					# --------------------
					if tmp["error"] or not tmp["response"]:
						retries -= 1
						if retries < 1:
							failure.append(entry)
					else:
						retries = 0
						entry["results"] = self.__parse_response(record, tmp["response"])
						if entry["results"]:
							success.append(entry)
					# --------------------
					await context.clear_cookies() # anti-bot evasion 3
					# --------------------
		except (PlaywrightError, Exception) as ex:
			self.__print_error(ex)
		finally:
			if context:
				await context.close()
			if browser:
				await browser.close()
			if pw:
				await pw.stop()
		self.__extend_data(success, failure)

	async def __set_context(self, browser):
		return await browser.new_context(
			ignore_https_errors = True,
			java_script_enabled = True,
			accept_downloads    = False,
			bypass_csp          = False
		)

	def __get_headers(self):
		return {
			"Accept": "*/*",
			"Accept-Language": "*",
			"Connection": "keep-alive",
			"Referer": "https://www.google.com/",
			# "Upgrade-Insecure-Requests": "1", # some websites might return incorrect page content because of this request header
			"User-Agent": self.__get_user_agent()
		}

	def __get_user_agent(self):
		return self.__user_agents[random.randint(0, self.__user_agents_len - 1)]

	async def __page_get(self, context, url):
		tmp = {"response": None, "error": False}
		page = None
		try:
			page = await context.new_page()
			await page.route("**/*", self.__block) # block unnecessary requests
			response = await page.goto(url)
			if self.__wait:
				await asyncio.sleep(self.__wait)
			await page.wait_for_load_state(state = "load")
			try:
				await page.wait_for_load_state(state = "networkidle") # wait until network is idle for 500ms within 30s
			except PlaywrightTimeoutError: # live streams will always timeout
				pass
			tmp["response"] = await page.content()
			self.__print_status(response.status, url)
		except PlaywrightTimeoutError:
			pass
		except (PlaywrightError, Exception) as ex: # break and fallback in case of invalid domain or file access
			tmp["error"] = True
			self.__print_error(ex)
		finally:
			if page:
				await page.close()
		return tmp

	async def __block(self, route):
		if route.request.resource_type in ["fetch", "stylesheet", "image", "ping", "font", "media", "imageset", "beacon", "csp_report", "object", "texttrack", "manifest"]:
			await route.abort()
		else:
			await route.continue_()

	async def __request_get(self, context, url):
		tmp = {"response": None, "error": False}
		try:
			response = await context.request.get(url)
			body = await response.body()
			tmp["response"] = body.decode(encoding)
			self.__print_status(response.status, url)
		except PlaywrightTimeoutError:
			pass
		except (PlaywrightError, Exception) as ex: # break in case of request timeout or invalid domain
			tmp["error"] = True
			self.__print_error(ex)
		return tmp

	def __print_status(self, key, value):
		if self.__debug:
			with self.__debug_lock:
				termcolor.cprint(("{0}: {1}").format(key, value), "yellow")

	def __print_error(self, error):
		if self.__debug:
			with self.__debug_lock:
				termcolor.cprint(error, "red")

	def __print_lock(self, text):
		with self.__debug_lock:
			print(text)

	def save_results(self, plaintext = False):
		extracted         = self.__keys["data"]["extract" ]["success"]
		failed_extraction = self.__keys["data"]["extract" ]["failure"]
		extract_error     = self.__keys["data"]["extract" ]["error"  ]
		validated         = self.__keys["data"]["validate"]["success"]
		failed_validation = self.__keys["data"]["validate"]["failure"]
		validate_error    = self.__keys["data"]["validate"]["error"  ]
		tmp               = self.__get_report(plaintext)
		# --------------------------------
		self.__data[extracted]    = jquery(self.__data[extracted], "sort_by_file" if plaintext else "sort_by_url")
		tmp["full"   ]            = self.__data[extracted] if plaintext else jquery(self.__data[extracted], "delete_files")
		tmp["summary"][extracted] = unique(jquery(tmp["full"], "select_results"), sort = True)
		# --------------------------------
		if not plaintext:
			self.__data[failed_extraction] = jquery(self.__data[failed_extraction], "sort_by_url")
			tmp["failed"][extract_error]   = jquery(self.__data[failed_extraction], "select_url")
		# --------------------------------
		self.__data[validated]    = jquery(self.__data[validated], "sort_by_url")
		tmp["summary"][validated] = jquery(self.__data[validated], "select_url")
		# --------------------------------
		self.__data[failed_validation] = jquery(self.__data[failed_validation], "sort_by_url")
		tmp["failed"][validate_error]  = jquery(self.__data[failed_validation], "select_url")
		# --------------------------------
		write_file(jdump(tmp), self.__out)
		# --------------------------------
		if self.__verbose:
			for file in jquery(self.__data[extracted], "select_file" if plaintext else "select_files"):
				# ------------------------
				tmp = self.__get_report(plaintext, main = False)
				# ------------------------
				if not plaintext:
					tmp["full"   ]              = jquery(self.__data[extracted], "select_by_file_delete_files", file)
					tmp["summary"]["extracted"] = jquery(tmp["full"], "select_results", sort = True)
				else:
					obj                         = jquery(self.__data[extracted], "select_by_file", file)
					tmp["summary"]["extracted"] = jquery(obj, "select_results", sort = True)
					tmp["results"]              = obj[0]["results"]
				# ------------------------
				if not plaintext:
					tmp["failed"][extract_error] = jquery(self.__data[failed_extraction], "select_url_by_file", file)
				# ------------------------
				tmp["summary"][validated] = jquery(self.__data[validated], "select_url_by_file", file)
				# ------------------------
				tmp["failed"][validate_error] = jquery(self.__data[failed_validation], "select_url_by_file", file)
				# ------------------------
				write_file_silent(jdump(tmp), file.rsplit(".", 1)[0] + self.__extension)
				# ------------------------

	def __get_report(self, plaintext = False, main = True):
		extracted      = self.__keys["data"]["extract" ]["success"]
		extract_error  = self.__keys["data"]["extract" ]["error"  ]
		validated      = self.__keys["data"]["validate"]["success"]
		validate_error = self.__keys["data"]["validate"]["error"  ]
		# --------------------------------
		tmp = {
			"started_at": stopwatch.get_start().strftime("%Y-%m-%d %H:%M:%S"),
			"summary": {
				validated: [],
				extracted: []
			},
			"failed": {
				validate_error: []
			},
			"full": {}
		}
		if not plaintext:
			tmp["failed"][extract_error] = []
		elif not main:
			tmp.pop("full")
			tmp["results"] = {}
		return tmp

# ----------------------------------------

class MyArgParser(argparse.ArgumentParser):

	def print_help(self):
		print("Chad Extractor v5.7 ( github.com/ivan-sincek/chad )")
		print("")
		print("Usage:   chad-extractor -t template      -res results      -o out                 [-th threads] [-r retries] [-w wait]")
		print("Example: chad-extractor -t template.json -res chad_results -o results_report.json [-th 10     ] [-r 5      ] [-w 10  ]")
		print("")
		print("DESCRIPTION")
		print("    Extract and validate data from Chad results or plaintext files")
		print("TEMPLATE")
		print("    JSON template file with extraction and validation information")
		print("    -t, --template = template.json | etc.")
		print("RESULTS")
		print("    Directory containing Chad results or plaintext files, or a single file")
		print("    In case of a directory, files ending with '.report.json' will be ignored")
		print("    -res, --results = chad_results | results.json | urls.txt | etc.")
		print("PLAINTEXT")
		print("    Treat all the results as plaintext files")
		print("    -pt, --plaintext")
		print("EXCLUDES")
		print("    File with regular expressions or a single regular expression to exclude the page content")
		print("    Applies only on extraction")
		print("    -e, --excludes = regexes.txt | \"<div id=\\\"seo\\\">.+?<\\/div>\" | etc.")
		print("THREADS")
		print("    Number of parallel headless browsers to run")
		print("    Default: 4")
		print("    -th, --threads = 10 | etc.")
		print("RETRIES")
		print("    Number of retries per URL")
		print("    Default: 2")
		print("    -r, --retries = 5 | etc.")
		print("WAIT")
		print("    Wait time before returning the page content")
		print("    Default: 4")
		print("    -w, --wait = 10 | etc.")
		print("USER AGENTS")
		print("    File with user agents to use")
		print("    Default: random")
		print("    -a, --user-agents = user_agents.txt | etc.")
		print("PROXY")
		print("    Web proxy to use")
		print("    -x, --proxy = http://127.0.0.1:8080 | etc.")
		print("OUT")
		print("    Output file")
		print("    -o, --out = results_report.json | etc.")
		print("VERBOSE")
		print("    Create additional supporting output files")
		print("    -v, --verbose")
		print("DEBUG")
		print("    Debug output")
		print("    -dbg, --debug")

	def error(self, message):
		if len(sys.argv) > 1:
			print("Missing a mandatory option (-t, -res, -o) and/or optional (-pt, -e, -th, -r, -w, -a, -x, -v, -dbg)")
			print("Use -h or --help for more info")
		else:
			self.print_help()
		exit()

class Validate:

	def __init__(self):
		self.__extension = ".report.json"
		self.__proceed   = True
		self.__parser    = MyArgParser()
		self.__parser.add_argument("-t"  , "--template"   , required = True , type   = str         , default = ""   )
		self.__parser.add_argument("-res", "--results"    , required = True , type   = str         , default = ""   )
		self.__parser.add_argument("-pt" , "--plaintext"  , required = False, action = "store_true", default = False)
		self.__parser.add_argument("-e"  , "--excludes"   , required = False, type   = str         , default = ""   )
		self.__parser.add_argument("-th" , "--threads"    , required = False, type   = str         , default = ""   )
		self.__parser.add_argument("-r"  , "--retries"    , required = False, type   = str         , default = ""   )
		self.__parser.add_argument("-w"  , "--wait"       , required = False, type   = str         , default = ""   )
		self.__parser.add_argument("-a"  , "--user-agents", required = False, type   = str         , default = ""   )
		self.__parser.add_argument("-x"  , "--proxy"      , required = False, type   = str         , default = ""   )
		self.__parser.add_argument("-o"  , "--out"        , required = True , type   = str         , default = ""   )
		self.__parser.add_argument("-v"  , "--verbose"    , required = False, action = "store_true", default = False)
		self.__parser.add_argument("-dbg", "--debug"      , required = False, action = "store_true", default = False)

	def run(self):
		self.__args             = self.__parser.parse_args()
		self.__args.template    = self.__parse_template(self.__args.template)       # required
		self.__args.results     = self.__parse_results(self.__args.results)         # required
		self.__args.excludes    = self.__parse_excludes(self.__args.excludes)       if self.__args.excludes    else []
		self.__args.threads     = self.__parse_threads(self.__args.threads)         if self.__args.threads     else 4
		self.__args.retries     = self.__parse_retries(self.__args.retries)         if self.__args.retries     else 2
		self.__args.wait        = self.__parse_wait(self.__args.wait)               if self.__args.wait        else 4
		self.__args.user_agents = self.__parse_user_agents(self.__args.user_agents) if self.__args.user_agents else []
		self.__args.proxy       = self.__parse_proxy(self.__args.proxy)             if self.__args.proxy       else ""
		self.__args             = vars(self.__args)
		return self.__proceed

	def get_arg(self, key):
		return self.__args[key]

	def get_extension(self):
		return self.__extension

	def __error(self, msg):
		self.__proceed = False
		self.__print_error(msg)

	def __print_error(self, msg):
		print(("ERROR: {0}").format(msg))

	def __parse_template(self, value):
		tmp = {}
		if not os.path.isfile(value):
			self.__error("Template file does not exists")
		elif not os.access(value, os.R_OK):
			self.__error("Template file does not have a read permission")
		elif not os.stat(value).st_size > 0:
			self.__error("Template file is empty")
		else:
			tmp = jload_file(value)
			if not tmp:
				self.__error("Template file has invalid JSON format")
		return tmp

	def __parse_results(self, value):
		tmp = []
		if not os.path.exists(value):
			self.__error("Directory containing Chad results or plaintext files, or a single file does not exists")
		elif os.path.isdir(value):
			for file in check_directory_files(value):
				if not file.endswith(self.__extension):
					tmp.append(file)
			if not tmp:
				self.__error("No valid Chad results or plaintext files were found")
		else:
			if not os.access(value, os.R_OK):
				self.__error("Chad results or plaintext file does not have a read permission")
			elif not os.stat(value).st_size > 0:
				self.__error("Chad results or plaintext file is empty")
			else:
				tmp = [value]
		return tmp

	def __parse_regexes(self, values):
		if not isinstance(values, list):
			values = [values]
		try:
			for value in values:
				re.compile(value)
		except re.error as ex:
			self.__error("Invalid regular expression was detected")
		return values

	def __parse_excludes(self, value):
		tmp = []
		if os.path.isfile(value):
			if not os.access(value, os.R_OK):
				self.__error("File with regular expressions does not have a read permission")
			elif not os.stat(value).st_size > 0:
				self.__error("File with regular expressions is empty")
			else:
				tmp = read_file(value)
				if not tmp:
					self.__error("No regular expressions were found")
				else:
					tmp = self.__parse_regexes(tmp)
		else:
			tmp = self.__parse_regexes(value)
		return tmp

	def __parse_greater_than(self, value, minimum, maximum, error_numeric, error_scope):
		if not value.isdigit():
			self.__error(error_numeric)
		else:
			value = int(value)
			if (minimum and value < minimum) or (maximum and value > maximum):
				self.__error(error_scope)
		return value

	def __parse_threads(self, value):
		return self.__parse_greater_than(value, 1, None,
			"Number of parallel headless browsers must be numeric",
			"Number of parallel headless browsers must be greater than zero"
		)

	def __parse_retries(self, value):
		return self.__parse_greater_than(value, 0, None,
			"Number of retries per URL must be numeric",
			"Number of retries per URL must be greater than or equal to zero"
		)

	def __parse_wait(self, value):
		return self.__parse_greater_than(value, 0, None,
			"Wait time before fetching the page content must be numeric",
			"Wait time before fetching the page content must be greater than or equal to zero"
		)

	def __parse_user_agents(self, value):
		tmp = []
		if not os.path.isfile(value):
			self.__error("File with user agents does not exists")
		elif not os.access(value, os.R_OK):
			self.__error("File with user agents does not have a read permission")
		elif not os.stat(value).st_size > 0:
			self.__error("File with user agents is empty")
		else:
			tmp = read_file(value)
			if not tmp:
				self.__error("No user agents were found")
		return tmp

	def __parse_proxy(self, value):
		tmp = urllib.parse.urlsplit(value)
		if not tmp.scheme:
			self.__error("Proxy URL: Scheme is required")
		elif tmp.scheme not in ["http", "https", "socks4", "socks4h", "socks5", "socks5h"]:
			self.__error("Proxy URL: Supported schemes are 'http[s]', 'socks4[h]', and 'socks5[h]'")
		elif not tmp.netloc:
			self.__error("Proxy URL: Invalid domain name")
		elif tmp.port and (tmp.port < 1 or tmp.port > 65535):
			self.__error("Proxy URL: Port number is out of range")
		return value

# ----------------------------------------

def main():
	validate = Validate()
	if validate.run():
		print("###########################################################################")
		print("#                                                                         #")
		print("#                           Chad Extractor v5.7                           #")
		print("#                                   by Ivan Sincek                        #")
		print("#                                                                         #")
		print("# Extract and validate data from Chad results.                            #")
		print("# GitHub repository at github.com/ivan-sincek/chad.                       #")
		print("# Feel free to donate ETH at 0xbc00e800f29524AD8b0968CEBEAD4cD5C5c1f105.  #")
		print("#                                                                         #")
		print("###########################################################################")
		chad_extractor = ChadExtractor(
			validate.get_arg("template"),
			validate.get_arg("results"),
			validate.get_arg("excludes"),
			validate.get_arg("threads"),
			validate.get_arg("retries"),
			validate.get_arg("wait"),
			validate.get_arg("user_agents"),
			validate.get_arg("proxy"),
			validate.get_arg("out"),
			validate.get_extension(),
			validate.get_arg("verbose"),
			validate.get_arg("debug")
		)
		if validate.get_arg("plaintext"):
			if not chad_extractor.parse_template():
				print("No extraction entries were found in the template file")
			elif not chad_extractor.parse_input(plaintext = True):
				print("No data was extracted")
			else:
				chad_extractor.set_validate()
				if not chad_extractor.parse_template():
					print("No validation entries were found in the template file")
				elif not chad_extractor.parse_input(plaintext = True):
					print("No results for data validation were found")
				elif not chad_extractor.run():
					print("No data matched the validation criteria")
				chad_extractor.save_results(plaintext = True)
		else:
			if not chad_extractor.parse_template():
				print("No extraction entries were found in the template file")
			elif not chad_extractor.parse_input():
				print("No results for data extraction were found")
			elif not chad_extractor.run():
				print("No data was extracted")
			else:
				chad_extractor.set_validate()
				if not chad_extractor.parse_template():
					print("No validation entries were found in the template file")
				elif not chad_extractor.parse_input():
					print("No results for data validation were found")
				elif not chad_extractor.run():
					print("No data matched the validation criteria")
				chad_extractor.save_results()
		stopwatch.stop()

if __name__ == "__main__":
	main()
