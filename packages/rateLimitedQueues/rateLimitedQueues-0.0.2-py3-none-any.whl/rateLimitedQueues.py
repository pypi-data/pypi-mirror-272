__version__ = "0.0.2"
__packagename__ = "rateLimitedQueues"


def updatePackage():
    from time import sleep
    from json import loads
    import http.client
    print(f"Checking updates for Package {__packagename__}")
    try:
        host = "pypi.org"
        conn = http.client.HTTPSConnection(host, 443)
        conn.request("GET", f"/pypi/{__packagename__}/json")
        data = loads(conn.getresponse().read())
        latest = data['info']['version']
        if latest != __version__:
            try:
                import pip
                pip.main(["install", __packagename__, "--upgrade"])
                print(f"\nUpdated package {__packagename__} v{__version__} to v{latest}\nPlease restart the program for changes to take effect")
                sleep(3)
            except:
                print(f"\nFailed to update package {__packagename__} v{__version__} (Latest: v{latest})\nPlease consider using pip install {__packagename__} --upgrade")
                sleep(3)
        else:
            print(f"Package {__packagename__} already the latest version")
    except:
        print(f"Ignoring version check for {__packagename__} (Failed)")


class Imports:
    from typing import Any, Callable
    from time import sleep, time
    from threading import Thread


class Manager:
    def __init__(self, timeBetweenExecution:float=0, smallestWaitTime:float=0):
        """
        Initialises a rate limiter cum queued event executor
        :param timeBetweenExecution: Time to wait between concurrent executions. By default, executed immediately without any time wait.
        :param smallestWaitTime: any time duration greater than 0 and less than `smallestWaitTime` will automatically be changed to `smallestWaitTime` to prevent warnings for example libuv needs smallestWaitTime to be 0.001
        """
        self.__executorIdle = True
        self.__tasks:dict[int, list[list[Imports.Callable | tuple[Imports.Any] | dict[str, Imports.Any]]]] = {}
        self.maxRateLimitWaitDuration = timeBetweenExecution
        self.minRateLimitWaitDuration = smallestWaitTime
        self.lastExecutionAt = 0


    def __startExecution(self) -> None:
        """
        Private method to start executing all pending actions. Runs only one instance of executor. Executes only the oldest task with the highest priority. Handles all time limits.
        :return:
        """
        if self.__executorIdle: self.__executorIdle = False
        else: return
        while self.__tasks:
            topPriority = max(self.__tasks)
            task = self.__tasks[topPriority].pop()
            if not self.__tasks[topPriority]: self.__tasks.pop(topPriority)
            mainFunction, args, kwargs, executeThreaded, postFunction, postArgs, postKwArgs = task
            if postKwArgs is None: postKwArgs = {}
            if postArgs is None: postArgs = ()
            if self.maxRateLimitWaitDuration > 0:
                while True:
                    toSleep = self.maxRateLimitWaitDuration - (Imports.time() - self.lastExecutionAt)
                    if toSleep > 0:
                        if toSleep > self.minRateLimitWaitDuration: Imports.sleep(toSleep)
                        else: Imports.sleep(self.minRateLimitWaitDuration)
                    else: break
            if executeThreaded: Imports.Thread(target=mainFunction, args=args, kwargs=kwargs).start()
            else: postKwArgs.update({"functionResponse": mainFunction(*args, **kwargs)})
            if postFunction is not None: Imports.Thread(target=postFunction, args=postArgs, kwargs=postKwArgs).start()
            self.lastExecutionAt = Imports.time()
        self.__executorIdle = True


    def queueAction(self, mainFunction, executePriority:int=0, executeThreaded: bool = False, postFunction = None, postArgs:tuple = None, postKwArgs:dict = None, *args, **kwargs):
        """
        Queue here.
        :param mainFunction: The function to be run when it reaches its turn.
        :param executePriority: Priority for execution. High priority tasks are executed before low priority ones. There's no limit for highest or lowest value.
        :param executeThreaded: Function is executed in a new thread. If True Rate limit is calculated from the start of execution, and output from the function can't be fetched. If False Rate limit is calculated from ending of execution of the function, also output from function can be fetched
        and passed if needed.
        :param postFunction: A second function(optional) to execute when the main function starts to execute(if Threaded) else after the main function is executed(if not Threaded). postFunction, if passed, is always executed in a new thread.
        :param postArgs: Arguments to pass only to the postFunction. Must be a tuple.
        :param postKwArgs: Keyword-Arguments to pass only to the postFunction. Must be a tuple.
        :param args: All additional arguments to be passed to mainFunction
        :param kwargs: All additional keyword-arguments to be passed to mainFunction
        :return:
        """
        if not callable(mainFunction): return print("Please pass a callable object as the `mainFunction` parameter...")
        if postFunction is not None and not callable(postFunction): return print("Please pass a callable object as the `postFunction` parameter...")
        if postArgs is not None and type(postArgs)!=tuple: return print("Please pass a tuple as postArgs...")
        if postKwArgs is not None and type(postKwArgs)!=dict: return print("Please pass a dictionary as postKwArgs...")
        execList = [mainFunction, args, kwargs, executeThreaded, postFunction, postArgs, postKwArgs]
        if executePriority in self.__tasks: self.__tasks[executePriority].append(execList)
        else: self.__tasks[executePriority] = [execList]
        Imports.Thread(target=self.__startExecution).start()
