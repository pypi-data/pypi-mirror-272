/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ 265:
/***/ ((module) => {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncaught exception popping up in devtools
	return Promise.resolve().then(() => {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	});
}
webpackEmptyAsyncContext.keys = () => ([]);
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = 265;
module.exports = webpackEmptyAsyncContext;

/***/ }),

/***/ 18673:
/***/ ((__unused_webpack_module, __unused_webpack___webpack_exports__, __webpack_require__) => {

"use strict";

;// CONCATENATED MODULE: ./node_modules/comlink/dist/esm/comlink.mjs
/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
const proxyMarker = Symbol("Comlink.proxy");
const createEndpoint = Symbol("Comlink.endpoint");
const releaseProxy = Symbol("Comlink.releaseProxy");
const finalizer = Symbol("Comlink.finalizer");
const throwMarker = Symbol("Comlink.thrown");
const isObject = (val) => (typeof val === "object" && val !== null) || typeof val === "function";
/**
 * Internal transfer handle to handle objects marked to proxy.
 */
const proxyTransferHandler = {
    canHandle: (val) => isObject(val) && val[proxyMarker],
    serialize(obj) {
        const { port1, port2 } = new MessageChannel();
        expose(obj, port1);
        return [port2, [port2]];
    },
    deserialize(port) {
        port.start();
        return wrap(port);
    },
};
/**
 * Internal transfer handler to handle thrown exceptions.
 */
const throwTransferHandler = {
    canHandle: (value) => isObject(value) && throwMarker in value,
    serialize({ value }) {
        let serialized;
        if (value instanceof Error) {
            serialized = {
                isError: true,
                value: {
                    message: value.message,
                    name: value.name,
                    stack: value.stack,
                },
            };
        }
        else {
            serialized = { isError: false, value };
        }
        return [serialized, []];
    },
    deserialize(serialized) {
        if (serialized.isError) {
            throw Object.assign(new Error(serialized.value.message), serialized.value);
        }
        throw serialized.value;
    },
};
/**
 * Allows customizing the serialization of certain values.
 */
const transferHandlers = new Map([
    ["proxy", proxyTransferHandler],
    ["throw", throwTransferHandler],
]);
function isAllowedOrigin(allowedOrigins, origin) {
    for (const allowedOrigin of allowedOrigins) {
        if (origin === allowedOrigin || allowedOrigin === "*") {
            return true;
        }
        if (allowedOrigin instanceof RegExp && allowedOrigin.test(origin)) {
            return true;
        }
    }
    return false;
}
function expose(obj, ep = globalThis, allowedOrigins = ["*"]) {
    ep.addEventListener("message", function callback(ev) {
        if (!ev || !ev.data) {
            return;
        }
        if (!isAllowedOrigin(allowedOrigins, ev.origin)) {
            console.warn(`Invalid origin '${ev.origin}' for comlink proxy`);
            return;
        }
        const { id, type, path } = Object.assign({ path: [] }, ev.data);
        const argumentList = (ev.data.argumentList || []).map(fromWireValue);
        let returnValue;
        try {
            const parent = path.slice(0, -1).reduce((obj, prop) => obj[prop], obj);
            const rawValue = path.reduce((obj, prop) => obj[prop], obj);
            switch (type) {
                case "GET" /* MessageType.GET */:
                    {
                        returnValue = rawValue;
                    }
                    break;
                case "SET" /* MessageType.SET */:
                    {
                        parent[path.slice(-1)[0]] = fromWireValue(ev.data.value);
                        returnValue = true;
                    }
                    break;
                case "APPLY" /* MessageType.APPLY */:
                    {
                        returnValue = rawValue.apply(parent, argumentList);
                    }
                    break;
                case "CONSTRUCT" /* MessageType.CONSTRUCT */:
                    {
                        const value = new rawValue(...argumentList);
                        returnValue = proxy(value);
                    }
                    break;
                case "ENDPOINT" /* MessageType.ENDPOINT */:
                    {
                        const { port1, port2 } = new MessageChannel();
                        expose(obj, port2);
                        returnValue = transfer(port1, [port1]);
                    }
                    break;
                case "RELEASE" /* MessageType.RELEASE */:
                    {
                        returnValue = undefined;
                    }
                    break;
                default:
                    return;
            }
        }
        catch (value) {
            returnValue = { value, [throwMarker]: 0 };
        }
        Promise.resolve(returnValue)
            .catch((value) => {
            return { value, [throwMarker]: 0 };
        })
            .then((returnValue) => {
            const [wireValue, transferables] = toWireValue(returnValue);
            ep.postMessage(Object.assign(Object.assign({}, wireValue), { id }), transferables);
            if (type === "RELEASE" /* MessageType.RELEASE */) {
                // detach and deactive after sending release response above.
                ep.removeEventListener("message", callback);
                closeEndPoint(ep);
                if (finalizer in obj && typeof obj[finalizer] === "function") {
                    obj[finalizer]();
                }
            }
        })
            .catch((error) => {
            // Send Serialization Error To Caller
            const [wireValue, transferables] = toWireValue({
                value: new TypeError("Unserializable return value"),
                [throwMarker]: 0,
            });
            ep.postMessage(Object.assign(Object.assign({}, wireValue), { id }), transferables);
        });
    });
    if (ep.start) {
        ep.start();
    }
}
function isMessagePort(endpoint) {
    return endpoint.constructor.name === "MessagePort";
}
function closeEndPoint(endpoint) {
    if (isMessagePort(endpoint))
        endpoint.close();
}
function wrap(ep, target) {
    return createProxy(ep, [], target);
}
function throwIfProxyReleased(isReleased) {
    if (isReleased) {
        throw new Error("Proxy has been released and is not useable");
    }
}
function releaseEndpoint(ep) {
    return requestResponseMessage(ep, {
        type: "RELEASE" /* MessageType.RELEASE */,
    }).then(() => {
        closeEndPoint(ep);
    });
}
const proxyCounter = new WeakMap();
const proxyFinalizers = "FinalizationRegistry" in globalThis &&
    new FinalizationRegistry((ep) => {
        const newCount = (proxyCounter.get(ep) || 0) - 1;
        proxyCounter.set(ep, newCount);
        if (newCount === 0) {
            releaseEndpoint(ep);
        }
    });
function registerProxy(proxy, ep) {
    const newCount = (proxyCounter.get(ep) || 0) + 1;
    proxyCounter.set(ep, newCount);
    if (proxyFinalizers) {
        proxyFinalizers.register(proxy, ep, proxy);
    }
}
function unregisterProxy(proxy) {
    if (proxyFinalizers) {
        proxyFinalizers.unregister(proxy);
    }
}
function createProxy(ep, path = [], target = function () { }) {
    let isProxyReleased = false;
    const proxy = new Proxy(target, {
        get(_target, prop) {
            throwIfProxyReleased(isProxyReleased);
            if (prop === releaseProxy) {
                return () => {
                    unregisterProxy(proxy);
                    releaseEndpoint(ep);
                    isProxyReleased = true;
                };
            }
            if (prop === "then") {
                if (path.length === 0) {
                    return { then: () => proxy };
                }
                const r = requestResponseMessage(ep, {
                    type: "GET" /* MessageType.GET */,
                    path: path.map((p) => p.toString()),
                }).then(fromWireValue);
                return r.then.bind(r);
            }
            return createProxy(ep, [...path, prop]);
        },
        set(_target, prop, rawValue) {
            throwIfProxyReleased(isProxyReleased);
            // FIXME: ES6 Proxy Handler `set` methods are supposed to return a
            // boolean. To show good will, we return true asynchronously ¯\_(ツ)_/¯
            const [value, transferables] = toWireValue(rawValue);
            return requestResponseMessage(ep, {
                type: "SET" /* MessageType.SET */,
                path: [...path, prop].map((p) => p.toString()),
                value,
            }, transferables).then(fromWireValue);
        },
        apply(_target, _thisArg, rawArgumentList) {
            throwIfProxyReleased(isProxyReleased);
            const last = path[path.length - 1];
            if (last === createEndpoint) {
                return requestResponseMessage(ep, {
                    type: "ENDPOINT" /* MessageType.ENDPOINT */,
                }).then(fromWireValue);
            }
            // We just pretend that `bind()` didn’t happen.
            if (last === "bind") {
                return createProxy(ep, path.slice(0, -1));
            }
            const [argumentList, transferables] = processArguments(rawArgumentList);
            return requestResponseMessage(ep, {
                type: "APPLY" /* MessageType.APPLY */,
                path: path.map((p) => p.toString()),
                argumentList,
            }, transferables).then(fromWireValue);
        },
        construct(_target, rawArgumentList) {
            throwIfProxyReleased(isProxyReleased);
            const [argumentList, transferables] = processArguments(rawArgumentList);
            return requestResponseMessage(ep, {
                type: "CONSTRUCT" /* MessageType.CONSTRUCT */,
                path: path.map((p) => p.toString()),
                argumentList,
            }, transferables).then(fromWireValue);
        },
    });
    registerProxy(proxy, ep);
    return proxy;
}
function myFlat(arr) {
    return Array.prototype.concat.apply([], arr);
}
function processArguments(argumentList) {
    const processed = argumentList.map(toWireValue);
    return [processed.map((v) => v[0]), myFlat(processed.map((v) => v[1]))];
}
const transferCache = new WeakMap();
function transfer(obj, transfers) {
    transferCache.set(obj, transfers);
    return obj;
}
function proxy(obj) {
    return Object.assign(obj, { [proxyMarker]: true });
}
function windowEndpoint(w, context = globalThis, targetOrigin = "*") {
    return {
        postMessage: (msg, transferables) => w.postMessage(msg, targetOrigin, transferables),
        addEventListener: context.addEventListener.bind(context),
        removeEventListener: context.removeEventListener.bind(context),
    };
}
function toWireValue(value) {
    for (const [name, handler] of transferHandlers) {
        if (handler.canHandle(value)) {
            const [serializedValue, transferables] = handler.serialize(value);
            return [
                {
                    type: "HANDLER" /* WireValueType.HANDLER */,
                    name,
                    value: serializedValue,
                },
                transferables,
            ];
        }
    }
    return [
        {
            type: "RAW" /* WireValueType.RAW */,
            value,
        },
        transferCache.get(value) || [],
    ];
}
function fromWireValue(value) {
    switch (value.type) {
        case "HANDLER" /* WireValueType.HANDLER */:
            return transferHandlers.get(value.name).deserialize(value.value);
        case "RAW" /* WireValueType.RAW */:
            return value.value;
    }
}
function requestResponseMessage(ep, msg, transfers) {
    return new Promise((resolve) => {
        const id = generateUUID();
        ep.addEventListener("message", function l(ev) {
            if (!ev.data || !ev.data.id || ev.data.id !== id) {
                return;
            }
            ep.removeEventListener("message", l);
            resolve(ev.data);
        });
        if (ep.start) {
            ep.start();
        }
        ep.postMessage(Object.assign({ id }, msg), transfers);
    });
}
function generateUUID() {
    return new Array(4)
        .fill(0)
        .map(() => Math.floor(Math.random() * Number.MAX_SAFE_INTEGER).toString(16))
        .join("-");
}


//# sourceMappingURL=comlink.mjs.map

// EXTERNAL MODULE: ./node_modules/@jupyterlite/pyodide-kernel/lib/worker.js
var worker = __webpack_require__(87179);
;// CONCATENATED MODULE: ./node_modules/@jupyterlite/pyodide-kernel/lib/comlink.worker.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * A WebWorker entrypoint that uses comlink to handle postMessage details
 */


const comlink_worker_worker = new worker/* PyodideRemoteKernel */.O();
expose(comlink_worker_worker);

/***/ }),

/***/ 95545:
/***/ ((module) => {

// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;
function defaultSetTimout() {
  throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout() {
  throw new Error('clearTimeout has not been defined');
}
(function () {
  try {
    if (typeof setTimeout === 'function') {
      cachedSetTimeout = setTimeout;
    } else {
      cachedSetTimeout = defaultSetTimout;
    }
  } catch (e) {
    cachedSetTimeout = defaultSetTimout;
  }
  try {
    if (typeof clearTimeout === 'function') {
      cachedClearTimeout = clearTimeout;
    } else {
      cachedClearTimeout = defaultClearTimeout;
    }
  } catch (e) {
    cachedClearTimeout = defaultClearTimeout;
  }
})();
function runTimeout(fun) {
  if (cachedSetTimeout === setTimeout) {
    //normal enviroments in sane situations
    return setTimeout(fun, 0);
  }
  // if setTimeout wasn't available but was latter defined
  if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
    cachedSetTimeout = setTimeout;
    return setTimeout(fun, 0);
  }
  try {
    // when when somebody has screwed with setTimeout but no I.E. maddness
    return cachedSetTimeout(fun, 0);
  } catch (e) {
    try {
      // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
      return cachedSetTimeout.call(null, fun, 0);
    } catch (e) {
      // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
      return cachedSetTimeout.call(this, fun, 0);
    }
  }
}
function runClearTimeout(marker) {
  if (cachedClearTimeout === clearTimeout) {
    //normal enviroments in sane situations
    return clearTimeout(marker);
  }
  // if clearTimeout wasn't available but was latter defined
  if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
    cachedClearTimeout = clearTimeout;
    return clearTimeout(marker);
  }
  try {
    // when when somebody has screwed with setTimeout but no I.E. maddness
    return cachedClearTimeout(marker);
  } catch (e) {
    try {
      // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
      return cachedClearTimeout.call(null, marker);
    } catch (e) {
      // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
      // Some versions of I.E. have different rules for clearTimeout vs setTimeout
      return cachedClearTimeout.call(this, marker);
    }
  }
}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;
function cleanUpNextTick() {
  if (!draining || !currentQueue) {
    return;
  }
  draining = false;
  if (currentQueue.length) {
    queue = currentQueue.concat(queue);
  } else {
    queueIndex = -1;
  }
  if (queue.length) {
    drainQueue();
  }
}
function drainQueue() {
  if (draining) {
    return;
  }
  var timeout = runTimeout(cleanUpNextTick);
  draining = true;
  var len = queue.length;
  while (len) {
    currentQueue = queue;
    queue = [];
    while (++queueIndex < len) {
      if (currentQueue) {
        currentQueue[queueIndex].run();
      }
    }
    queueIndex = -1;
    len = queue.length;
  }
  currentQueue = null;
  draining = false;
  runClearTimeout(timeout);
}
process.nextTick = function (fun) {
  var args = new Array(arguments.length - 1);
  if (arguments.length > 1) {
    for (var i = 1; i < arguments.length; i++) {
      args[i - 1] = arguments[i];
    }
  }
  queue.push(new Item(fun, args));
  if (queue.length === 1 && !draining) {
    runTimeout(drainQueue);
  }
};

// v8 likes predictible objects
function Item(fun, array) {
  this.fun = fun;
  this.array = array;
}
Item.prototype.run = function () {
  this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};
function noop() {}
process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;
process.listeners = function (name) {
  return [];
};
process.binding = function (name) {
  throw new Error('process.binding is not supported');
};
process.cwd = function () {
  return '/';
};
process.chdir = function (dir) {
  throw new Error('process.chdir is not supported');
};
process.umask = function () {
  return 0;
};

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// the startup function
/******/ 	__webpack_require__.x = () => {
/******/ 		// Load entry module and return exports
/******/ 		// This entry module depends on other loaded chunks and execution need to be delayed
/******/ 		var __webpack_exports__ = __webpack_require__.O(undefined, [7179], () => (__webpack_require__(18673)))
/******/ 		__webpack_exports__ = __webpack_require__.O(__webpack_exports__);
/******/ 		return __webpack_exports__;
/******/ 	};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/amd options */
/******/ 	(() => {
/******/ 		__webpack_require__.amdO = {};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/chunk loaded */
/******/ 	(() => {
/******/ 		var deferred = [];
/******/ 		__webpack_require__.O = (result, chunkIds, fn, priority) => {
/******/ 			if(chunkIds) {
/******/ 				priority = priority || 0;
/******/ 				for(var i = deferred.length; i > 0 && deferred[i - 1][2] > priority; i--) deferred[i] = deferred[i - 1];
/******/ 				deferred[i] = [chunkIds, fn, priority];
/******/ 				return;
/******/ 			}
/******/ 			var notFulfilled = Infinity;
/******/ 			for (var i = 0; i < deferred.length; i++) {
/******/ 				var [chunkIds, fn, priority] = deferred[i];
/******/ 				var fulfilled = true;
/******/ 				for (var j = 0; j < chunkIds.length; j++) {
/******/ 					if ((priority & 1 === 0 || notFulfilled >= priority) && Object.keys(__webpack_require__.O).every((key) => (__webpack_require__.O[key](chunkIds[j])))) {
/******/ 						chunkIds.splice(j--, 1);
/******/ 					} else {
/******/ 						fulfilled = false;
/******/ 						if(priority < notFulfilled) notFulfilled = priority;
/******/ 					}
/******/ 				}
/******/ 				if(fulfilled) {
/******/ 					deferred.splice(i--, 1)
/******/ 					var r = fn();
/******/ 					if (r !== undefined) result = r;
/******/ 				}
/******/ 			}
/******/ 			return result;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks and sibling chunks for the entrypoint
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + ".jupyter-viewer.js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		__webpack_require__.p = "/static/jupyter_viewer/";
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/importScripts chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded chunks
/******/ 		// "1" means "already loaded"
/******/ 		var installedChunks = {
/******/ 			3596: 1
/******/ 		};
/******/ 		
/******/ 		// importScripts chunk loading
/******/ 		var installChunk = (data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			for(var moduleId in moreModules) {
/******/ 				if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 					__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 				}
/******/ 			}
/******/ 			if(runtime) runtime(__webpack_require__);
/******/ 			while(chunkIds.length)
/******/ 				installedChunks[chunkIds.pop()] = 1;
/******/ 			parentChunkLoadingFunction(data);
/******/ 		};
/******/ 		__webpack_require__.f.i = (chunkId, promises) => {
/******/ 			// "1" is the signal for "already loaded"
/******/ 			if(!installedChunks[chunkId]) {
/******/ 				if(true) { // all chunks have JS
/******/ 					importScripts(__webpack_require__.p + __webpack_require__.u(chunkId));
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || [];
/******/ 		var parentChunkLoadingFunction = chunkLoadingGlobal.push.bind(chunkLoadingGlobal);
/******/ 		chunkLoadingGlobal.push = installChunk;
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/startup chunk dependencies */
/******/ 	(() => {
/******/ 		var next = __webpack_require__.x;
/******/ 		__webpack_require__.x = () => {
/******/ 			return __webpack_require__.e(7179).then(next);
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// run startup
/******/ 	var __webpack_exports__ = __webpack_require__.x();
/******/ 	
/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzU5Ni5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7Ozs7OztBQ1pBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7OztBQ3pWQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUNSQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7O0FDOUtBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7OztBQ25DQTs7Ozs7QUNBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7QUMzQkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7QUNQQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7O0FDUkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7QUNKQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7OztBQ1BBOzs7OztBQ0FBOzs7OztBQ0FBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7OztBQ3BDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7QUVIQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AanVweXRlcmxpdGUvcHlvZGlkZS1rZXJuZWwvbGliLyBsYXp5IG5hbWVzcGFjZSBvYmplY3QiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9jb21saW5rL2Rpc3QvZXNtL2NvbWxpbmsubWpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGp1cHl0ZXJsaXRlL3B5b2RpZGUta2VybmVsL2xpYi9jb21saW5rLndvcmtlci5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL3Byb2Nlc3MvYnJvd3Nlci5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyL3dlYnBhY2svYm9vdHN0cmFwIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvd2VicGFjay9ydW50aW1lL2FtZCBvcHRpb25zIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvd2VicGFjay9ydW50aW1lL2NodW5rIGxvYWRlZCIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyL3dlYnBhY2svcnVudGltZS9kZWZpbmUgcHJvcGVydHkgZ2V0dGVycyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyL3dlYnBhY2svcnVudGltZS9lbnN1cmUgY2h1bmsiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci93ZWJwYWNrL3J1bnRpbWUvZ2V0IGphdmFzY3JpcHQgY2h1bmsgZmlsZW5hbWUiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci93ZWJwYWNrL3J1bnRpbWUvZ2xvYmFsIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvd2VicGFjay9ydW50aW1lL2hhc093blByb3BlcnR5IHNob3J0aGFuZCIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyL3dlYnBhY2svcnVudGltZS9wdWJsaWNQYXRoIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvd2VicGFjay9ydW50aW1lL2ltcG9ydFNjcmlwdHMgY2h1bmsgbG9hZGluZyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyL3dlYnBhY2svcnVudGltZS9zdGFydHVwIGNodW5rIGRlcGVuZGVuY2llcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyL3dlYnBhY2svYmVmb3JlLXN0YXJ0dXAiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci93ZWJwYWNrL3N0YXJ0dXAiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci93ZWJwYWNrL2FmdGVyLXN0YXJ0dXAiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd2VicGFja0VtcHR5QXN5bmNDb250ZXh0KHJlcSkge1xuXHQvLyBIZXJlIFByb21pc2UucmVzb2x2ZSgpLnRoZW4oKSBpcyB1c2VkIGluc3RlYWQgb2YgbmV3IFByb21pc2UoKSB0byBwcmV2ZW50XG5cdC8vIHVuY2F1Z2h0IGV4Y2VwdGlvbiBwb3BwaW5nIHVwIGluIGRldnRvb2xzXG5cdHJldHVybiBQcm9taXNlLnJlc29sdmUoKS50aGVuKCgpID0+IHtcblx0XHR2YXIgZSA9IG5ldyBFcnJvcihcIkNhbm5vdCBmaW5kIG1vZHVsZSAnXCIgKyByZXEgKyBcIidcIik7XG5cdFx0ZS5jb2RlID0gJ01PRFVMRV9OT1RfRk9VTkQnO1xuXHRcdHRocm93IGU7XG5cdH0pO1xufVxud2VicGFja0VtcHR5QXN5bmNDb250ZXh0LmtleXMgPSAoKSA9PiAoW10pO1xud2VicGFja0VtcHR5QXN5bmNDb250ZXh0LnJlc29sdmUgPSB3ZWJwYWNrRW1wdHlBc3luY0NvbnRleHQ7XG53ZWJwYWNrRW1wdHlBc3luY0NvbnRleHQuaWQgPSAyNjU7XG5tb2R1bGUuZXhwb3J0cyA9IHdlYnBhY2tFbXB0eUFzeW5jQ29udGV4dDsiLCIvKipcbiAqIEBsaWNlbnNlXG4gKiBDb3B5cmlnaHQgMjAxOSBHb29nbGUgTExDXG4gKiBTUERYLUxpY2Vuc2UtSWRlbnRpZmllcjogQXBhY2hlLTIuMFxuICovXG5jb25zdCBwcm94eU1hcmtlciA9IFN5bWJvbChcIkNvbWxpbmsucHJveHlcIik7XG5jb25zdCBjcmVhdGVFbmRwb2ludCA9IFN5bWJvbChcIkNvbWxpbmsuZW5kcG9pbnRcIik7XG5jb25zdCByZWxlYXNlUHJveHkgPSBTeW1ib2woXCJDb21saW5rLnJlbGVhc2VQcm94eVwiKTtcbmNvbnN0IGZpbmFsaXplciA9IFN5bWJvbChcIkNvbWxpbmsuZmluYWxpemVyXCIpO1xuY29uc3QgdGhyb3dNYXJrZXIgPSBTeW1ib2woXCJDb21saW5rLnRocm93blwiKTtcbmNvbnN0IGlzT2JqZWN0ID0gKHZhbCkgPT4gKHR5cGVvZiB2YWwgPT09IFwib2JqZWN0XCIgJiYgdmFsICE9PSBudWxsKSB8fCB0eXBlb2YgdmFsID09PSBcImZ1bmN0aW9uXCI7XG4vKipcbiAqIEludGVybmFsIHRyYW5zZmVyIGhhbmRsZSB0byBoYW5kbGUgb2JqZWN0cyBtYXJrZWQgdG8gcHJveHkuXG4gKi9cbmNvbnN0IHByb3h5VHJhbnNmZXJIYW5kbGVyID0ge1xuICAgIGNhbkhhbmRsZTogKHZhbCkgPT4gaXNPYmplY3QodmFsKSAmJiB2YWxbcHJveHlNYXJrZXJdLFxuICAgIHNlcmlhbGl6ZShvYmopIHtcbiAgICAgICAgY29uc3QgeyBwb3J0MSwgcG9ydDIgfSA9IG5ldyBNZXNzYWdlQ2hhbm5lbCgpO1xuICAgICAgICBleHBvc2Uob2JqLCBwb3J0MSk7XG4gICAgICAgIHJldHVybiBbcG9ydDIsIFtwb3J0Ml1dO1xuICAgIH0sXG4gICAgZGVzZXJpYWxpemUocG9ydCkge1xuICAgICAgICBwb3J0LnN0YXJ0KCk7XG4gICAgICAgIHJldHVybiB3cmFwKHBvcnQpO1xuICAgIH0sXG59O1xuLyoqXG4gKiBJbnRlcm5hbCB0cmFuc2ZlciBoYW5kbGVyIHRvIGhhbmRsZSB0aHJvd24gZXhjZXB0aW9ucy5cbiAqL1xuY29uc3QgdGhyb3dUcmFuc2ZlckhhbmRsZXIgPSB7XG4gICAgY2FuSGFuZGxlOiAodmFsdWUpID0+IGlzT2JqZWN0KHZhbHVlKSAmJiB0aHJvd01hcmtlciBpbiB2YWx1ZSxcbiAgICBzZXJpYWxpemUoeyB2YWx1ZSB9KSB7XG4gICAgICAgIGxldCBzZXJpYWxpemVkO1xuICAgICAgICBpZiAodmFsdWUgaW5zdGFuY2VvZiBFcnJvcikge1xuICAgICAgICAgICAgc2VyaWFsaXplZCA9IHtcbiAgICAgICAgICAgICAgICBpc0Vycm9yOiB0cnVlLFxuICAgICAgICAgICAgICAgIHZhbHVlOiB7XG4gICAgICAgICAgICAgICAgICAgIG1lc3NhZ2U6IHZhbHVlLm1lc3NhZ2UsXG4gICAgICAgICAgICAgICAgICAgIG5hbWU6IHZhbHVlLm5hbWUsXG4gICAgICAgICAgICAgICAgICAgIHN0YWNrOiB2YWx1ZS5zdGFjayxcbiAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgfTtcbiAgICAgICAgfVxuICAgICAgICBlbHNlIHtcbiAgICAgICAgICAgIHNlcmlhbGl6ZWQgPSB7IGlzRXJyb3I6IGZhbHNlLCB2YWx1ZSB9O1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBbc2VyaWFsaXplZCwgW11dO1xuICAgIH0sXG4gICAgZGVzZXJpYWxpemUoc2VyaWFsaXplZCkge1xuICAgICAgICBpZiAoc2VyaWFsaXplZC5pc0Vycm9yKSB7XG4gICAgICAgICAgICB0aHJvdyBPYmplY3QuYXNzaWduKG5ldyBFcnJvcihzZXJpYWxpemVkLnZhbHVlLm1lc3NhZ2UpLCBzZXJpYWxpemVkLnZhbHVlKTtcbiAgICAgICAgfVxuICAgICAgICB0aHJvdyBzZXJpYWxpemVkLnZhbHVlO1xuICAgIH0sXG59O1xuLyoqXG4gKiBBbGxvd3MgY3VzdG9taXppbmcgdGhlIHNlcmlhbGl6YXRpb24gb2YgY2VydGFpbiB2YWx1ZXMuXG4gKi9cbmNvbnN0IHRyYW5zZmVySGFuZGxlcnMgPSBuZXcgTWFwKFtcbiAgICBbXCJwcm94eVwiLCBwcm94eVRyYW5zZmVySGFuZGxlcl0sXG4gICAgW1widGhyb3dcIiwgdGhyb3dUcmFuc2ZlckhhbmRsZXJdLFxuXSk7XG5mdW5jdGlvbiBpc0FsbG93ZWRPcmlnaW4oYWxsb3dlZE9yaWdpbnMsIG9yaWdpbikge1xuICAgIGZvciAoY29uc3QgYWxsb3dlZE9yaWdpbiBvZiBhbGxvd2VkT3JpZ2lucykge1xuICAgICAgICBpZiAob3JpZ2luID09PSBhbGxvd2VkT3JpZ2luIHx8IGFsbG93ZWRPcmlnaW4gPT09IFwiKlwiKSB7XG4gICAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoYWxsb3dlZE9yaWdpbiBpbnN0YW5jZW9mIFJlZ0V4cCAmJiBhbGxvd2VkT3JpZ2luLnRlc3Qob3JpZ2luKSkge1xuICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGZhbHNlO1xufVxuZnVuY3Rpb24gZXhwb3NlKG9iaiwgZXAgPSBnbG9iYWxUaGlzLCBhbGxvd2VkT3JpZ2lucyA9IFtcIipcIl0pIHtcbiAgICBlcC5hZGRFdmVudExpc3RlbmVyKFwibWVzc2FnZVwiLCBmdW5jdGlvbiBjYWxsYmFjayhldikge1xuICAgICAgICBpZiAoIWV2IHx8ICFldi5kYXRhKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgaWYgKCFpc0FsbG93ZWRPcmlnaW4oYWxsb3dlZE9yaWdpbnMsIGV2Lm9yaWdpbikpIHtcbiAgICAgICAgICAgIGNvbnNvbGUud2FybihgSW52YWxpZCBvcmlnaW4gJyR7ZXYub3JpZ2lufScgZm9yIGNvbWxpbmsgcHJveHlgKTtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCB7IGlkLCB0eXBlLCBwYXRoIH0gPSBPYmplY3QuYXNzaWduKHsgcGF0aDogW10gfSwgZXYuZGF0YSk7XG4gICAgICAgIGNvbnN0IGFyZ3VtZW50TGlzdCA9IChldi5kYXRhLmFyZ3VtZW50TGlzdCB8fCBbXSkubWFwKGZyb21XaXJlVmFsdWUpO1xuICAgICAgICBsZXQgcmV0dXJuVmFsdWU7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgICBjb25zdCBwYXJlbnQgPSBwYXRoLnNsaWNlKDAsIC0xKS5yZWR1Y2UoKG9iaiwgcHJvcCkgPT4gb2JqW3Byb3BdLCBvYmopO1xuICAgICAgICAgICAgY29uc3QgcmF3VmFsdWUgPSBwYXRoLnJlZHVjZSgob2JqLCBwcm9wKSA9PiBvYmpbcHJvcF0sIG9iaik7XG4gICAgICAgICAgICBzd2l0Y2ggKHR5cGUpIHtcbiAgICAgICAgICAgICAgICBjYXNlIFwiR0VUXCIgLyogTWVzc2FnZVR5cGUuR0VUICovOlxuICAgICAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm5WYWx1ZSA9IHJhd1ZhbHVlO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgICAgIGNhc2UgXCJTRVRcIiAvKiBNZXNzYWdlVHlwZS5TRVQgKi86XG4gICAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHBhcmVudFtwYXRoLnNsaWNlKC0xKVswXV0gPSBmcm9tV2lyZVZhbHVlKGV2LmRhdGEudmFsdWUpO1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuVmFsdWUgPSB0cnVlO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgICAgIGNhc2UgXCJBUFBMWVwiIC8qIE1lc3NhZ2VUeXBlLkFQUExZICovOlxuICAgICAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm5WYWx1ZSA9IHJhd1ZhbHVlLmFwcGx5KHBhcmVudCwgYXJndW1lbnRMaXN0KTtcbiAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgICAgICBjYXNlIFwiQ09OU1RSVUNUXCIgLyogTWVzc2FnZVR5cGUuQ09OU1RSVUNUICovOlxuICAgICAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgICAgICBjb25zdCB2YWx1ZSA9IG5ldyByYXdWYWx1ZSguLi5hcmd1bWVudExpc3QpO1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuVmFsdWUgPSBwcm94eSh2YWx1ZSk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgY2FzZSBcIkVORFBPSU5UXCIgLyogTWVzc2FnZVR5cGUuRU5EUE9JTlQgKi86XG4gICAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbnN0IHsgcG9ydDEsIHBvcnQyIH0gPSBuZXcgTWVzc2FnZUNoYW5uZWwoKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIGV4cG9zZShvYmosIHBvcnQyKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVyblZhbHVlID0gdHJhbnNmZXIocG9ydDEsIFtwb3J0MV0pO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgICAgIGNhc2UgXCJSRUxFQVNFXCIgLyogTWVzc2FnZVR5cGUuUkVMRUFTRSAqLzpcbiAgICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuVmFsdWUgPSB1bmRlZmluZWQ7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgZGVmYXVsdDpcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGNhdGNoICh2YWx1ZSkge1xuICAgICAgICAgICAgcmV0dXJuVmFsdWUgPSB7IHZhbHVlLCBbdGhyb3dNYXJrZXJdOiAwIH07XG4gICAgICAgIH1cbiAgICAgICAgUHJvbWlzZS5yZXNvbHZlKHJldHVyblZhbHVlKVxuICAgICAgICAgICAgLmNhdGNoKCh2YWx1ZSkgPT4ge1xuICAgICAgICAgICAgcmV0dXJuIHsgdmFsdWUsIFt0aHJvd01hcmtlcl06IDAgfTtcbiAgICAgICAgfSlcbiAgICAgICAgICAgIC50aGVuKChyZXR1cm5WYWx1ZSkgPT4ge1xuICAgICAgICAgICAgY29uc3QgW3dpcmVWYWx1ZSwgdHJhbnNmZXJhYmxlc10gPSB0b1dpcmVWYWx1ZShyZXR1cm5WYWx1ZSk7XG4gICAgICAgICAgICBlcC5wb3N0TWVzc2FnZShPYmplY3QuYXNzaWduKE9iamVjdC5hc3NpZ24oe30sIHdpcmVWYWx1ZSksIHsgaWQgfSksIHRyYW5zZmVyYWJsZXMpO1xuICAgICAgICAgICAgaWYgKHR5cGUgPT09IFwiUkVMRUFTRVwiIC8qIE1lc3NhZ2VUeXBlLlJFTEVBU0UgKi8pIHtcbiAgICAgICAgICAgICAgICAvLyBkZXRhY2ggYW5kIGRlYWN0aXZlIGFmdGVyIHNlbmRpbmcgcmVsZWFzZSByZXNwb25zZSBhYm92ZS5cbiAgICAgICAgICAgICAgICBlcC5yZW1vdmVFdmVudExpc3RlbmVyKFwibWVzc2FnZVwiLCBjYWxsYmFjayk7XG4gICAgICAgICAgICAgICAgY2xvc2VFbmRQb2ludChlcCk7XG4gICAgICAgICAgICAgICAgaWYgKGZpbmFsaXplciBpbiBvYmogJiYgdHlwZW9mIG9ialtmaW5hbGl6ZXJdID09PSBcImZ1bmN0aW9uXCIpIHtcbiAgICAgICAgICAgICAgICAgICAgb2JqW2ZpbmFsaXplcl0oKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH0pXG4gICAgICAgICAgICAuY2F0Y2goKGVycm9yKSA9PiB7XG4gICAgICAgICAgICAvLyBTZW5kIFNlcmlhbGl6YXRpb24gRXJyb3IgVG8gQ2FsbGVyXG4gICAgICAgICAgICBjb25zdCBbd2lyZVZhbHVlLCB0cmFuc2ZlcmFibGVzXSA9IHRvV2lyZVZhbHVlKHtcbiAgICAgICAgICAgICAgICB2YWx1ZTogbmV3IFR5cGVFcnJvcihcIlVuc2VyaWFsaXphYmxlIHJldHVybiB2YWx1ZVwiKSxcbiAgICAgICAgICAgICAgICBbdGhyb3dNYXJrZXJdOiAwLFxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICBlcC5wb3N0TWVzc2FnZShPYmplY3QuYXNzaWduKE9iamVjdC5hc3NpZ24oe30sIHdpcmVWYWx1ZSksIHsgaWQgfSksIHRyYW5zZmVyYWJsZXMpO1xuICAgICAgICB9KTtcbiAgICB9KTtcbiAgICBpZiAoZXAuc3RhcnQpIHtcbiAgICAgICAgZXAuc3RhcnQoKTtcbiAgICB9XG59XG5mdW5jdGlvbiBpc01lc3NhZ2VQb3J0KGVuZHBvaW50KSB7XG4gICAgcmV0dXJuIGVuZHBvaW50LmNvbnN0cnVjdG9yLm5hbWUgPT09IFwiTWVzc2FnZVBvcnRcIjtcbn1cbmZ1bmN0aW9uIGNsb3NlRW5kUG9pbnQoZW5kcG9pbnQpIHtcbiAgICBpZiAoaXNNZXNzYWdlUG9ydChlbmRwb2ludCkpXG4gICAgICAgIGVuZHBvaW50LmNsb3NlKCk7XG59XG5mdW5jdGlvbiB3cmFwKGVwLCB0YXJnZXQpIHtcbiAgICByZXR1cm4gY3JlYXRlUHJveHkoZXAsIFtdLCB0YXJnZXQpO1xufVxuZnVuY3Rpb24gdGhyb3dJZlByb3h5UmVsZWFzZWQoaXNSZWxlYXNlZCkge1xuICAgIGlmIChpc1JlbGVhc2VkKSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcihcIlByb3h5IGhhcyBiZWVuIHJlbGVhc2VkIGFuZCBpcyBub3QgdXNlYWJsZVwiKTtcbiAgICB9XG59XG5mdW5jdGlvbiByZWxlYXNlRW5kcG9pbnQoZXApIHtcbiAgICByZXR1cm4gcmVxdWVzdFJlc3BvbnNlTWVzc2FnZShlcCwge1xuICAgICAgICB0eXBlOiBcIlJFTEVBU0VcIiAvKiBNZXNzYWdlVHlwZS5SRUxFQVNFICovLFxuICAgIH0pLnRoZW4oKCkgPT4ge1xuICAgICAgICBjbG9zZUVuZFBvaW50KGVwKTtcbiAgICB9KTtcbn1cbmNvbnN0IHByb3h5Q291bnRlciA9IG5ldyBXZWFrTWFwKCk7XG5jb25zdCBwcm94eUZpbmFsaXplcnMgPSBcIkZpbmFsaXphdGlvblJlZ2lzdHJ5XCIgaW4gZ2xvYmFsVGhpcyAmJlxuICAgIG5ldyBGaW5hbGl6YXRpb25SZWdpc3RyeSgoZXApID0+IHtcbiAgICAgICAgY29uc3QgbmV3Q291bnQgPSAocHJveHlDb3VudGVyLmdldChlcCkgfHwgMCkgLSAxO1xuICAgICAgICBwcm94eUNvdW50ZXIuc2V0KGVwLCBuZXdDb3VudCk7XG4gICAgICAgIGlmIChuZXdDb3VudCA9PT0gMCkge1xuICAgICAgICAgICAgcmVsZWFzZUVuZHBvaW50KGVwKTtcbiAgICAgICAgfVxuICAgIH0pO1xuZnVuY3Rpb24gcmVnaXN0ZXJQcm94eShwcm94eSwgZXApIHtcbiAgICBjb25zdCBuZXdDb3VudCA9IChwcm94eUNvdW50ZXIuZ2V0KGVwKSB8fCAwKSArIDE7XG4gICAgcHJveHlDb3VudGVyLnNldChlcCwgbmV3Q291bnQpO1xuICAgIGlmIChwcm94eUZpbmFsaXplcnMpIHtcbiAgICAgICAgcHJveHlGaW5hbGl6ZXJzLnJlZ2lzdGVyKHByb3h5LCBlcCwgcHJveHkpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIHVucmVnaXN0ZXJQcm94eShwcm94eSkge1xuICAgIGlmIChwcm94eUZpbmFsaXplcnMpIHtcbiAgICAgICAgcHJveHlGaW5hbGl6ZXJzLnVucmVnaXN0ZXIocHJveHkpO1xuICAgIH1cbn1cbmZ1bmN0aW9uIGNyZWF0ZVByb3h5KGVwLCBwYXRoID0gW10sIHRhcmdldCA9IGZ1bmN0aW9uICgpIHsgfSkge1xuICAgIGxldCBpc1Byb3h5UmVsZWFzZWQgPSBmYWxzZTtcbiAgICBjb25zdCBwcm94eSA9IG5ldyBQcm94eSh0YXJnZXQsIHtcbiAgICAgICAgZ2V0KF90YXJnZXQsIHByb3ApIHtcbiAgICAgICAgICAgIHRocm93SWZQcm94eVJlbGVhc2VkKGlzUHJveHlSZWxlYXNlZCk7XG4gICAgICAgICAgICBpZiAocHJvcCA9PT0gcmVsZWFzZVByb3h5KSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuICgpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgdW5yZWdpc3RlclByb3h5KHByb3h5KTtcbiAgICAgICAgICAgICAgICAgICAgcmVsZWFzZUVuZHBvaW50KGVwKTtcbiAgICAgICAgICAgICAgICAgICAgaXNQcm94eVJlbGVhc2VkID0gdHJ1ZTtcbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKHByb3AgPT09IFwidGhlblwiKSB7XG4gICAgICAgICAgICAgICAgaWYgKHBhdGgubGVuZ3RoID09PSAwKSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiB7IHRoZW46ICgpID0+IHByb3h5IH07XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGNvbnN0IHIgPSByZXF1ZXN0UmVzcG9uc2VNZXNzYWdlKGVwLCB7XG4gICAgICAgICAgICAgICAgICAgIHR5cGU6IFwiR0VUXCIgLyogTWVzc2FnZVR5cGUuR0VUICovLFxuICAgICAgICAgICAgICAgICAgICBwYXRoOiBwYXRoLm1hcCgocCkgPT4gcC50b1N0cmluZygpKSxcbiAgICAgICAgICAgICAgICB9KS50aGVuKGZyb21XaXJlVmFsdWUpO1xuICAgICAgICAgICAgICAgIHJldHVybiByLnRoZW4uYmluZChyKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiBjcmVhdGVQcm94eShlcCwgWy4uLnBhdGgsIHByb3BdKTtcbiAgICAgICAgfSxcbiAgICAgICAgc2V0KF90YXJnZXQsIHByb3AsIHJhd1ZhbHVlKSB7XG4gICAgICAgICAgICB0aHJvd0lmUHJveHlSZWxlYXNlZChpc1Byb3h5UmVsZWFzZWQpO1xuICAgICAgICAgICAgLy8gRklYTUU6IEVTNiBQcm94eSBIYW5kbGVyIGBzZXRgIG1ldGhvZHMgYXJlIHN1cHBvc2VkIHRvIHJldHVybiBhXG4gICAgICAgICAgICAvLyBib29sZWFuLiBUbyBzaG93IGdvb2Qgd2lsbCwgd2UgcmV0dXJuIHRydWUgYXN5bmNocm9ub3VzbHkgwq9cXF8o44OEKV8vwq9cbiAgICAgICAgICAgIGNvbnN0IFt2YWx1ZSwgdHJhbnNmZXJhYmxlc10gPSB0b1dpcmVWYWx1ZShyYXdWYWx1ZSk7XG4gICAgICAgICAgICByZXR1cm4gcmVxdWVzdFJlc3BvbnNlTWVzc2FnZShlcCwge1xuICAgICAgICAgICAgICAgIHR5cGU6IFwiU0VUXCIgLyogTWVzc2FnZVR5cGUuU0VUICovLFxuICAgICAgICAgICAgICAgIHBhdGg6IFsuLi5wYXRoLCBwcm9wXS5tYXAoKHApID0+IHAudG9TdHJpbmcoKSksXG4gICAgICAgICAgICAgICAgdmFsdWUsXG4gICAgICAgICAgICB9LCB0cmFuc2ZlcmFibGVzKS50aGVuKGZyb21XaXJlVmFsdWUpO1xuICAgICAgICB9LFxuICAgICAgICBhcHBseShfdGFyZ2V0LCBfdGhpc0FyZywgcmF3QXJndW1lbnRMaXN0KSB7XG4gICAgICAgICAgICB0aHJvd0lmUHJveHlSZWxlYXNlZChpc1Byb3h5UmVsZWFzZWQpO1xuICAgICAgICAgICAgY29uc3QgbGFzdCA9IHBhdGhbcGF0aC5sZW5ndGggLSAxXTtcbiAgICAgICAgICAgIGlmIChsYXN0ID09PSBjcmVhdGVFbmRwb2ludCkge1xuICAgICAgICAgICAgICAgIHJldHVybiByZXF1ZXN0UmVzcG9uc2VNZXNzYWdlKGVwLCB7XG4gICAgICAgICAgICAgICAgICAgIHR5cGU6IFwiRU5EUE9JTlRcIiAvKiBNZXNzYWdlVHlwZS5FTkRQT0lOVCAqLyxcbiAgICAgICAgICAgICAgICB9KS50aGVuKGZyb21XaXJlVmFsdWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgLy8gV2UganVzdCBwcmV0ZW5kIHRoYXQgYGJpbmQoKWAgZGlkbuKAmXQgaGFwcGVuLlxuICAgICAgICAgICAgaWYgKGxhc3QgPT09IFwiYmluZFwiKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIGNyZWF0ZVByb3h5KGVwLCBwYXRoLnNsaWNlKDAsIC0xKSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBjb25zdCBbYXJndW1lbnRMaXN0LCB0cmFuc2ZlcmFibGVzXSA9IHByb2Nlc3NBcmd1bWVudHMocmF3QXJndW1lbnRMaXN0KTtcbiAgICAgICAgICAgIHJldHVybiByZXF1ZXN0UmVzcG9uc2VNZXNzYWdlKGVwLCB7XG4gICAgICAgICAgICAgICAgdHlwZTogXCJBUFBMWVwiIC8qIE1lc3NhZ2VUeXBlLkFQUExZICovLFxuICAgICAgICAgICAgICAgIHBhdGg6IHBhdGgubWFwKChwKSA9PiBwLnRvU3RyaW5nKCkpLFxuICAgICAgICAgICAgICAgIGFyZ3VtZW50TGlzdCxcbiAgICAgICAgICAgIH0sIHRyYW5zZmVyYWJsZXMpLnRoZW4oZnJvbVdpcmVWYWx1ZSk7XG4gICAgICAgIH0sXG4gICAgICAgIGNvbnN0cnVjdChfdGFyZ2V0LCByYXdBcmd1bWVudExpc3QpIHtcbiAgICAgICAgICAgIHRocm93SWZQcm94eVJlbGVhc2VkKGlzUHJveHlSZWxlYXNlZCk7XG4gICAgICAgICAgICBjb25zdCBbYXJndW1lbnRMaXN0LCB0cmFuc2ZlcmFibGVzXSA9IHByb2Nlc3NBcmd1bWVudHMocmF3QXJndW1lbnRMaXN0KTtcbiAgICAgICAgICAgIHJldHVybiByZXF1ZXN0UmVzcG9uc2VNZXNzYWdlKGVwLCB7XG4gICAgICAgICAgICAgICAgdHlwZTogXCJDT05TVFJVQ1RcIiAvKiBNZXNzYWdlVHlwZS5DT05TVFJVQ1QgKi8sXG4gICAgICAgICAgICAgICAgcGF0aDogcGF0aC5tYXAoKHApID0+IHAudG9TdHJpbmcoKSksXG4gICAgICAgICAgICAgICAgYXJndW1lbnRMaXN0LFxuICAgICAgICAgICAgfSwgdHJhbnNmZXJhYmxlcykudGhlbihmcm9tV2lyZVZhbHVlKTtcbiAgICAgICAgfSxcbiAgICB9KTtcbiAgICByZWdpc3RlclByb3h5KHByb3h5LCBlcCk7XG4gICAgcmV0dXJuIHByb3h5O1xufVxuZnVuY3Rpb24gbXlGbGF0KGFycikge1xuICAgIHJldHVybiBBcnJheS5wcm90b3R5cGUuY29uY2F0LmFwcGx5KFtdLCBhcnIpO1xufVxuZnVuY3Rpb24gcHJvY2Vzc0FyZ3VtZW50cyhhcmd1bWVudExpc3QpIHtcbiAgICBjb25zdCBwcm9jZXNzZWQgPSBhcmd1bWVudExpc3QubWFwKHRvV2lyZVZhbHVlKTtcbiAgICByZXR1cm4gW3Byb2Nlc3NlZC5tYXAoKHYpID0+IHZbMF0pLCBteUZsYXQocHJvY2Vzc2VkLm1hcCgodikgPT4gdlsxXSkpXTtcbn1cbmNvbnN0IHRyYW5zZmVyQ2FjaGUgPSBuZXcgV2Vha01hcCgpO1xuZnVuY3Rpb24gdHJhbnNmZXIob2JqLCB0cmFuc2ZlcnMpIHtcbiAgICB0cmFuc2ZlckNhY2hlLnNldChvYmosIHRyYW5zZmVycyk7XG4gICAgcmV0dXJuIG9iajtcbn1cbmZ1bmN0aW9uIHByb3h5KG9iaikge1xuICAgIHJldHVybiBPYmplY3QuYXNzaWduKG9iaiwgeyBbcHJveHlNYXJrZXJdOiB0cnVlIH0pO1xufVxuZnVuY3Rpb24gd2luZG93RW5kcG9pbnQodywgY29udGV4dCA9IGdsb2JhbFRoaXMsIHRhcmdldE9yaWdpbiA9IFwiKlwiKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgICAgcG9zdE1lc3NhZ2U6IChtc2csIHRyYW5zZmVyYWJsZXMpID0+IHcucG9zdE1lc3NhZ2UobXNnLCB0YXJnZXRPcmlnaW4sIHRyYW5zZmVyYWJsZXMpLFxuICAgICAgICBhZGRFdmVudExpc3RlbmVyOiBjb250ZXh0LmFkZEV2ZW50TGlzdGVuZXIuYmluZChjb250ZXh0KSxcbiAgICAgICAgcmVtb3ZlRXZlbnRMaXN0ZW5lcjogY29udGV4dC5yZW1vdmVFdmVudExpc3RlbmVyLmJpbmQoY29udGV4dCksXG4gICAgfTtcbn1cbmZ1bmN0aW9uIHRvV2lyZVZhbHVlKHZhbHVlKSB7XG4gICAgZm9yIChjb25zdCBbbmFtZSwgaGFuZGxlcl0gb2YgdHJhbnNmZXJIYW5kbGVycykge1xuICAgICAgICBpZiAoaGFuZGxlci5jYW5IYW5kbGUodmFsdWUpKSB7XG4gICAgICAgICAgICBjb25zdCBbc2VyaWFsaXplZFZhbHVlLCB0cmFuc2ZlcmFibGVzXSA9IGhhbmRsZXIuc2VyaWFsaXplKHZhbHVlKTtcbiAgICAgICAgICAgIHJldHVybiBbXG4gICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICB0eXBlOiBcIkhBTkRMRVJcIiAvKiBXaXJlVmFsdWVUeXBlLkhBTkRMRVIgKi8sXG4gICAgICAgICAgICAgICAgICAgIG5hbWUsXG4gICAgICAgICAgICAgICAgICAgIHZhbHVlOiBzZXJpYWxpemVkVmFsdWUsXG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICB0cmFuc2ZlcmFibGVzLFxuICAgICAgICAgICAgXTtcbiAgICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gW1xuICAgICAgICB7XG4gICAgICAgICAgICB0eXBlOiBcIlJBV1wiIC8qIFdpcmVWYWx1ZVR5cGUuUkFXICovLFxuICAgICAgICAgICAgdmFsdWUsXG4gICAgICAgIH0sXG4gICAgICAgIHRyYW5zZmVyQ2FjaGUuZ2V0KHZhbHVlKSB8fCBbXSxcbiAgICBdO1xufVxuZnVuY3Rpb24gZnJvbVdpcmVWYWx1ZSh2YWx1ZSkge1xuICAgIHN3aXRjaCAodmFsdWUudHlwZSkge1xuICAgICAgICBjYXNlIFwiSEFORExFUlwiIC8qIFdpcmVWYWx1ZVR5cGUuSEFORExFUiAqLzpcbiAgICAgICAgICAgIHJldHVybiB0cmFuc2ZlckhhbmRsZXJzLmdldCh2YWx1ZS5uYW1lKS5kZXNlcmlhbGl6ZSh2YWx1ZS52YWx1ZSk7XG4gICAgICAgIGNhc2UgXCJSQVdcIiAvKiBXaXJlVmFsdWVUeXBlLlJBVyAqLzpcbiAgICAgICAgICAgIHJldHVybiB2YWx1ZS52YWx1ZTtcbiAgICB9XG59XG5mdW5jdGlvbiByZXF1ZXN0UmVzcG9uc2VNZXNzYWdlKGVwLCBtc2csIHRyYW5zZmVycykge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4ge1xuICAgICAgICBjb25zdCBpZCA9IGdlbmVyYXRlVVVJRCgpO1xuICAgICAgICBlcC5hZGRFdmVudExpc3RlbmVyKFwibWVzc2FnZVwiLCBmdW5jdGlvbiBsKGV2KSB7XG4gICAgICAgICAgICBpZiAoIWV2LmRhdGEgfHwgIWV2LmRhdGEuaWQgfHwgZXYuZGF0YS5pZCAhPT0gaWQpIHtcbiAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBlcC5yZW1vdmVFdmVudExpc3RlbmVyKFwibWVzc2FnZVwiLCBsKTtcbiAgICAgICAgICAgIHJlc29sdmUoZXYuZGF0YSk7XG4gICAgICAgIH0pO1xuICAgICAgICBpZiAoZXAuc3RhcnQpIHtcbiAgICAgICAgICAgIGVwLnN0YXJ0KCk7XG4gICAgICAgIH1cbiAgICAgICAgZXAucG9zdE1lc3NhZ2UoT2JqZWN0LmFzc2lnbih7IGlkIH0sIG1zZyksIHRyYW5zZmVycyk7XG4gICAgfSk7XG59XG5mdW5jdGlvbiBnZW5lcmF0ZVVVSUQoKSB7XG4gICAgcmV0dXJuIG5ldyBBcnJheSg0KVxuICAgICAgICAuZmlsbCgwKVxuICAgICAgICAubWFwKCgpID0+IE1hdGguZmxvb3IoTWF0aC5yYW5kb20oKSAqIE51bWJlci5NQVhfU0FGRV9JTlRFR0VSKS50b1N0cmluZygxNikpXG4gICAgICAgIC5qb2luKFwiLVwiKTtcbn1cblxuZXhwb3J0IHsgY3JlYXRlRW5kcG9pbnQsIGV4cG9zZSwgZmluYWxpemVyLCBwcm94eSwgcHJveHlNYXJrZXIsIHJlbGVhc2VQcm94eSwgdHJhbnNmZXIsIHRyYW5zZmVySGFuZGxlcnMsIHdpbmRvd0VuZHBvaW50LCB3cmFwIH07XG4vLyMgc291cmNlTWFwcGluZ1VSTD1jb21saW5rLm1qcy5tYXBcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQSBXZWJXb3JrZXIgZW50cnlwb2ludCB0aGF0IHVzZXMgY29tbGluayB0byBoYW5kbGUgcG9zdE1lc3NhZ2UgZGV0YWlsc1xuICovXG5pbXBvcnQgeyBleHBvc2UgfSBmcm9tICdjb21saW5rJztcbmltcG9ydCB7IFB5b2RpZGVSZW1vdGVLZXJuZWwgfSBmcm9tICcuL3dvcmtlcic7XG5jb25zdCB3b3JrZXIgPSBuZXcgUHlvZGlkZVJlbW90ZUtlcm5lbCgpO1xuZXhwb3NlKHdvcmtlcik7IiwiLy8gc2hpbSBmb3IgdXNpbmcgcHJvY2VzcyBpbiBicm93c2VyXG52YXIgcHJvY2VzcyA9IG1vZHVsZS5leHBvcnRzID0ge307XG5cbi8vIGNhY2hlZCBmcm9tIHdoYXRldmVyIGdsb2JhbCBpcyBwcmVzZW50IHNvIHRoYXQgdGVzdCBydW5uZXJzIHRoYXQgc3R1YiBpdFxuLy8gZG9uJ3QgYnJlYWsgdGhpbmdzLiAgQnV0IHdlIG5lZWQgdG8gd3JhcCBpdCBpbiBhIHRyeSBjYXRjaCBpbiBjYXNlIGl0IGlzXG4vLyB3cmFwcGVkIGluIHN0cmljdCBtb2RlIGNvZGUgd2hpY2ggZG9lc24ndCBkZWZpbmUgYW55IGdsb2JhbHMuICBJdCdzIGluc2lkZSBhXG4vLyBmdW5jdGlvbiBiZWNhdXNlIHRyeS9jYXRjaGVzIGRlb3B0aW1pemUgaW4gY2VydGFpbiBlbmdpbmVzLlxuXG52YXIgY2FjaGVkU2V0VGltZW91dDtcbnZhciBjYWNoZWRDbGVhclRpbWVvdXQ7XG5mdW5jdGlvbiBkZWZhdWx0U2V0VGltb3V0KCkge1xuICB0aHJvdyBuZXcgRXJyb3IoJ3NldFRpbWVvdXQgaGFzIG5vdCBiZWVuIGRlZmluZWQnKTtcbn1cbmZ1bmN0aW9uIGRlZmF1bHRDbGVhclRpbWVvdXQoKSB7XG4gIHRocm93IG5ldyBFcnJvcignY2xlYXJUaW1lb3V0IGhhcyBub3QgYmVlbiBkZWZpbmVkJyk7XG59XG4oZnVuY3Rpb24gKCkge1xuICB0cnkge1xuICAgIGlmICh0eXBlb2Ygc2V0VGltZW91dCA9PT0gJ2Z1bmN0aW9uJykge1xuICAgICAgY2FjaGVkU2V0VGltZW91dCA9IHNldFRpbWVvdXQ7XG4gICAgfSBlbHNlIHtcbiAgICAgIGNhY2hlZFNldFRpbWVvdXQgPSBkZWZhdWx0U2V0VGltb3V0O1xuICAgIH1cbiAgfSBjYXRjaCAoZSkge1xuICAgIGNhY2hlZFNldFRpbWVvdXQgPSBkZWZhdWx0U2V0VGltb3V0O1xuICB9XG4gIHRyeSB7XG4gICAgaWYgKHR5cGVvZiBjbGVhclRpbWVvdXQgPT09ICdmdW5jdGlvbicpIHtcbiAgICAgIGNhY2hlZENsZWFyVGltZW91dCA9IGNsZWFyVGltZW91dDtcbiAgICB9IGVsc2Uge1xuICAgICAgY2FjaGVkQ2xlYXJUaW1lb3V0ID0gZGVmYXVsdENsZWFyVGltZW91dDtcbiAgICB9XG4gIH0gY2F0Y2ggKGUpIHtcbiAgICBjYWNoZWRDbGVhclRpbWVvdXQgPSBkZWZhdWx0Q2xlYXJUaW1lb3V0O1xuICB9XG59KSgpO1xuZnVuY3Rpb24gcnVuVGltZW91dChmdW4pIHtcbiAgaWYgKGNhY2hlZFNldFRpbWVvdXQgPT09IHNldFRpbWVvdXQpIHtcbiAgICAvL25vcm1hbCBlbnZpcm9tZW50cyBpbiBzYW5lIHNpdHVhdGlvbnNcbiAgICByZXR1cm4gc2V0VGltZW91dChmdW4sIDApO1xuICB9XG4gIC8vIGlmIHNldFRpbWVvdXQgd2Fzbid0IGF2YWlsYWJsZSBidXQgd2FzIGxhdHRlciBkZWZpbmVkXG4gIGlmICgoY2FjaGVkU2V0VGltZW91dCA9PT0gZGVmYXVsdFNldFRpbW91dCB8fCAhY2FjaGVkU2V0VGltZW91dCkgJiYgc2V0VGltZW91dCkge1xuICAgIGNhY2hlZFNldFRpbWVvdXQgPSBzZXRUaW1lb3V0O1xuICAgIHJldHVybiBzZXRUaW1lb3V0KGZ1biwgMCk7XG4gIH1cbiAgdHJ5IHtcbiAgICAvLyB3aGVuIHdoZW4gc29tZWJvZHkgaGFzIHNjcmV3ZWQgd2l0aCBzZXRUaW1lb3V0IGJ1dCBubyBJLkUuIG1hZGRuZXNzXG4gICAgcmV0dXJuIGNhY2hlZFNldFRpbWVvdXQoZnVuLCAwKTtcbiAgfSBjYXRjaCAoZSkge1xuICAgIHRyeSB7XG4gICAgICAvLyBXaGVuIHdlIGFyZSBpbiBJLkUuIGJ1dCB0aGUgc2NyaXB0IGhhcyBiZWVuIGV2YWxlZCBzbyBJLkUuIGRvZXNuJ3QgdHJ1c3QgdGhlIGdsb2JhbCBvYmplY3Qgd2hlbiBjYWxsZWQgbm9ybWFsbHlcbiAgICAgIHJldHVybiBjYWNoZWRTZXRUaW1lb3V0LmNhbGwobnVsbCwgZnVuLCAwKTtcbiAgICB9IGNhdGNoIChlKSB7XG4gICAgICAvLyBzYW1lIGFzIGFib3ZlIGJ1dCB3aGVuIGl0J3MgYSB2ZXJzaW9uIG9mIEkuRS4gdGhhdCBtdXN0IGhhdmUgdGhlIGdsb2JhbCBvYmplY3QgZm9yICd0aGlzJywgaG9wZnVsbHkgb3VyIGNvbnRleHQgY29ycmVjdCBvdGhlcndpc2UgaXQgd2lsbCB0aHJvdyBhIGdsb2JhbCBlcnJvclxuICAgICAgcmV0dXJuIGNhY2hlZFNldFRpbWVvdXQuY2FsbCh0aGlzLCBmdW4sIDApO1xuICAgIH1cbiAgfVxufVxuZnVuY3Rpb24gcnVuQ2xlYXJUaW1lb3V0KG1hcmtlcikge1xuICBpZiAoY2FjaGVkQ2xlYXJUaW1lb3V0ID09PSBjbGVhclRpbWVvdXQpIHtcbiAgICAvL25vcm1hbCBlbnZpcm9tZW50cyBpbiBzYW5lIHNpdHVhdGlvbnNcbiAgICByZXR1cm4gY2xlYXJUaW1lb3V0KG1hcmtlcik7XG4gIH1cbiAgLy8gaWYgY2xlYXJUaW1lb3V0IHdhc24ndCBhdmFpbGFibGUgYnV0IHdhcyBsYXR0ZXIgZGVmaW5lZFxuICBpZiAoKGNhY2hlZENsZWFyVGltZW91dCA9PT0gZGVmYXVsdENsZWFyVGltZW91dCB8fCAhY2FjaGVkQ2xlYXJUaW1lb3V0KSAmJiBjbGVhclRpbWVvdXQpIHtcbiAgICBjYWNoZWRDbGVhclRpbWVvdXQgPSBjbGVhclRpbWVvdXQ7XG4gICAgcmV0dXJuIGNsZWFyVGltZW91dChtYXJrZXIpO1xuICB9XG4gIHRyeSB7XG4gICAgLy8gd2hlbiB3aGVuIHNvbWVib2R5IGhhcyBzY3Jld2VkIHdpdGggc2V0VGltZW91dCBidXQgbm8gSS5FLiBtYWRkbmVzc1xuICAgIHJldHVybiBjYWNoZWRDbGVhclRpbWVvdXQobWFya2VyKTtcbiAgfSBjYXRjaCAoZSkge1xuICAgIHRyeSB7XG4gICAgICAvLyBXaGVuIHdlIGFyZSBpbiBJLkUuIGJ1dCB0aGUgc2NyaXB0IGhhcyBiZWVuIGV2YWxlZCBzbyBJLkUuIGRvZXNuJ3QgIHRydXN0IHRoZSBnbG9iYWwgb2JqZWN0IHdoZW4gY2FsbGVkIG5vcm1hbGx5XG4gICAgICByZXR1cm4gY2FjaGVkQ2xlYXJUaW1lb3V0LmNhbGwobnVsbCwgbWFya2VyKTtcbiAgICB9IGNhdGNoIChlKSB7XG4gICAgICAvLyBzYW1lIGFzIGFib3ZlIGJ1dCB3aGVuIGl0J3MgYSB2ZXJzaW9uIG9mIEkuRS4gdGhhdCBtdXN0IGhhdmUgdGhlIGdsb2JhbCBvYmplY3QgZm9yICd0aGlzJywgaG9wZnVsbHkgb3VyIGNvbnRleHQgY29ycmVjdCBvdGhlcndpc2UgaXQgd2lsbCB0aHJvdyBhIGdsb2JhbCBlcnJvci5cbiAgICAgIC8vIFNvbWUgdmVyc2lvbnMgb2YgSS5FLiBoYXZlIGRpZmZlcmVudCBydWxlcyBmb3IgY2xlYXJUaW1lb3V0IHZzIHNldFRpbWVvdXRcbiAgICAgIHJldHVybiBjYWNoZWRDbGVhclRpbWVvdXQuY2FsbCh0aGlzLCBtYXJrZXIpO1xuICAgIH1cbiAgfVxufVxudmFyIHF1ZXVlID0gW107XG52YXIgZHJhaW5pbmcgPSBmYWxzZTtcbnZhciBjdXJyZW50UXVldWU7XG52YXIgcXVldWVJbmRleCA9IC0xO1xuZnVuY3Rpb24gY2xlYW5VcE5leHRUaWNrKCkge1xuICBpZiAoIWRyYWluaW5nIHx8ICFjdXJyZW50UXVldWUpIHtcbiAgICByZXR1cm47XG4gIH1cbiAgZHJhaW5pbmcgPSBmYWxzZTtcbiAgaWYgKGN1cnJlbnRRdWV1ZS5sZW5ndGgpIHtcbiAgICBxdWV1ZSA9IGN1cnJlbnRRdWV1ZS5jb25jYXQocXVldWUpO1xuICB9IGVsc2Uge1xuICAgIHF1ZXVlSW5kZXggPSAtMTtcbiAgfVxuICBpZiAocXVldWUubGVuZ3RoKSB7XG4gICAgZHJhaW5RdWV1ZSgpO1xuICB9XG59XG5mdW5jdGlvbiBkcmFpblF1ZXVlKCkge1xuICBpZiAoZHJhaW5pbmcpIHtcbiAgICByZXR1cm47XG4gIH1cbiAgdmFyIHRpbWVvdXQgPSBydW5UaW1lb3V0KGNsZWFuVXBOZXh0VGljayk7XG4gIGRyYWluaW5nID0gdHJ1ZTtcbiAgdmFyIGxlbiA9IHF1ZXVlLmxlbmd0aDtcbiAgd2hpbGUgKGxlbikge1xuICAgIGN1cnJlbnRRdWV1ZSA9IHF1ZXVlO1xuICAgIHF1ZXVlID0gW107XG4gICAgd2hpbGUgKCsrcXVldWVJbmRleCA8IGxlbikge1xuICAgICAgaWYgKGN1cnJlbnRRdWV1ZSkge1xuICAgICAgICBjdXJyZW50UXVldWVbcXVldWVJbmRleF0ucnVuKCk7XG4gICAgICB9XG4gICAgfVxuICAgIHF1ZXVlSW5kZXggPSAtMTtcbiAgICBsZW4gPSBxdWV1ZS5sZW5ndGg7XG4gIH1cbiAgY3VycmVudFF1ZXVlID0gbnVsbDtcbiAgZHJhaW5pbmcgPSBmYWxzZTtcbiAgcnVuQ2xlYXJUaW1lb3V0KHRpbWVvdXQpO1xufVxucHJvY2Vzcy5uZXh0VGljayA9IGZ1bmN0aW9uIChmdW4pIHtcbiAgdmFyIGFyZ3MgPSBuZXcgQXJyYXkoYXJndW1lbnRzLmxlbmd0aCAtIDEpO1xuICBpZiAoYXJndW1lbnRzLmxlbmd0aCA+IDEpIHtcbiAgICBmb3IgKHZhciBpID0gMTsgaSA8IGFyZ3VtZW50cy5sZW5ndGg7IGkrKykge1xuICAgICAgYXJnc1tpIC0gMV0gPSBhcmd1bWVudHNbaV07XG4gICAgfVxuICB9XG4gIHF1ZXVlLnB1c2gobmV3IEl0ZW0oZnVuLCBhcmdzKSk7XG4gIGlmIChxdWV1ZS5sZW5ndGggPT09IDEgJiYgIWRyYWluaW5nKSB7XG4gICAgcnVuVGltZW91dChkcmFpblF1ZXVlKTtcbiAgfVxufTtcblxuLy8gdjggbGlrZXMgcHJlZGljdGlibGUgb2JqZWN0c1xuZnVuY3Rpb24gSXRlbShmdW4sIGFycmF5KSB7XG4gIHRoaXMuZnVuID0gZnVuO1xuICB0aGlzLmFycmF5ID0gYXJyYXk7XG59XG5JdGVtLnByb3RvdHlwZS5ydW4gPSBmdW5jdGlvbiAoKSB7XG4gIHRoaXMuZnVuLmFwcGx5KG51bGwsIHRoaXMuYXJyYXkpO1xufTtcbnByb2Nlc3MudGl0bGUgPSAnYnJvd3Nlcic7XG5wcm9jZXNzLmJyb3dzZXIgPSB0cnVlO1xucHJvY2Vzcy5lbnYgPSB7fTtcbnByb2Nlc3MuYXJndiA9IFtdO1xucHJvY2Vzcy52ZXJzaW9uID0gJyc7IC8vIGVtcHR5IHN0cmluZyB0byBhdm9pZCByZWdleHAgaXNzdWVzXG5wcm9jZXNzLnZlcnNpb25zID0ge307XG5mdW5jdGlvbiBub29wKCkge31cbnByb2Nlc3Mub24gPSBub29wO1xucHJvY2Vzcy5hZGRMaXN0ZW5lciA9IG5vb3A7XG5wcm9jZXNzLm9uY2UgPSBub29wO1xucHJvY2Vzcy5vZmYgPSBub29wO1xucHJvY2Vzcy5yZW1vdmVMaXN0ZW5lciA9IG5vb3A7XG5wcm9jZXNzLnJlbW92ZUFsbExpc3RlbmVycyA9IG5vb3A7XG5wcm9jZXNzLmVtaXQgPSBub29wO1xucHJvY2Vzcy5wcmVwZW5kTGlzdGVuZXIgPSBub29wO1xucHJvY2Vzcy5wcmVwZW5kT25jZUxpc3RlbmVyID0gbm9vcDtcbnByb2Nlc3MubGlzdGVuZXJzID0gZnVuY3Rpb24gKG5hbWUpIHtcbiAgcmV0dXJuIFtdO1xufTtcbnByb2Nlc3MuYmluZGluZyA9IGZ1bmN0aW9uIChuYW1lKSB7XG4gIHRocm93IG5ldyBFcnJvcigncHJvY2Vzcy5iaW5kaW5nIGlzIG5vdCBzdXBwb3J0ZWQnKTtcbn07XG5wcm9jZXNzLmN3ZCA9IGZ1bmN0aW9uICgpIHtcbiAgcmV0dXJuICcvJztcbn07XG5wcm9jZXNzLmNoZGlyID0gZnVuY3Rpb24gKGRpcikge1xuICB0aHJvdyBuZXcgRXJyb3IoJ3Byb2Nlc3MuY2hkaXIgaXMgbm90IHN1cHBvcnRlZCcpO1xufTtcbnByb2Nlc3MudW1hc2sgPSBmdW5jdGlvbiAoKSB7XG4gIHJldHVybiAwO1xufTsiLCIvLyBUaGUgbW9kdWxlIGNhY2hlXG52YXIgX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fID0ge307XG5cbi8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG5mdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuXHR2YXIgY2FjaGVkTW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXTtcblx0aWYgKGNhY2hlZE1vZHVsZSAhPT0gdW5kZWZpbmVkKSB7XG5cdFx0cmV0dXJuIGNhY2hlZE1vZHVsZS5leHBvcnRzO1xuXHR9XG5cdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG5cdHZhciBtb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdID0ge1xuXHRcdC8vIG5vIG1vZHVsZS5pZCBuZWVkZWRcblx0XHQvLyBubyBtb2R1bGUubG9hZGVkIG5lZWRlZFxuXHRcdGV4cG9ydHM6IHt9XG5cdH07XG5cblx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG5cdF9fd2VicGFja19tb2R1bGVzX19bbW9kdWxlSWRdKG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG5cdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG5cdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbn1cblxuLy8gZXhwb3NlIHRoZSBtb2R1bGVzIG9iamVjdCAoX193ZWJwYWNrX21vZHVsZXNfXylcbl9fd2VicGFja19yZXF1aXJlX18ubSA9IF9fd2VicGFja19tb2R1bGVzX187XG5cbi8vIHRoZSBzdGFydHVwIGZ1bmN0aW9uXG5fX3dlYnBhY2tfcmVxdWlyZV9fLnggPSAoKSA9PiB7XG5cdC8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuXHQvLyBUaGlzIGVudHJ5IG1vZHVsZSBkZXBlbmRzIG9uIG90aGVyIGxvYWRlZCBjaHVua3MgYW5kIGV4ZWN1dGlvbiBuZWVkIHRvIGJlIGRlbGF5ZWRcblx0dmFyIF9fd2VicGFja19leHBvcnRzX18gPSBfX3dlYnBhY2tfcmVxdWlyZV9fLk8odW5kZWZpbmVkLCBbNzE3OV0sICgpID0+IChfX3dlYnBhY2tfcmVxdWlyZV9fKDE4NjczKSkpXG5cdF9fd2VicGFja19leHBvcnRzX18gPSBfX3dlYnBhY2tfcmVxdWlyZV9fLk8oX193ZWJwYWNrX2V4cG9ydHNfXyk7XG5cdHJldHVybiBfX3dlYnBhY2tfZXhwb3J0c19fO1xufTtcblxuIiwiX193ZWJwYWNrX3JlcXVpcmVfXy5hbWRPID0ge307IiwidmFyIGRlZmVycmVkID0gW107XG5fX3dlYnBhY2tfcmVxdWlyZV9fLk8gPSAocmVzdWx0LCBjaHVua0lkcywgZm4sIHByaW9yaXR5KSA9PiB7XG5cdGlmKGNodW5rSWRzKSB7XG5cdFx0cHJpb3JpdHkgPSBwcmlvcml0eSB8fCAwO1xuXHRcdGZvcih2YXIgaSA9IGRlZmVycmVkLmxlbmd0aDsgaSA+IDAgJiYgZGVmZXJyZWRbaSAtIDFdWzJdID4gcHJpb3JpdHk7IGktLSkgZGVmZXJyZWRbaV0gPSBkZWZlcnJlZFtpIC0gMV07XG5cdFx0ZGVmZXJyZWRbaV0gPSBbY2h1bmtJZHMsIGZuLCBwcmlvcml0eV07XG5cdFx0cmV0dXJuO1xuXHR9XG5cdHZhciBub3RGdWxmaWxsZWQgPSBJbmZpbml0eTtcblx0Zm9yICh2YXIgaSA9IDA7IGkgPCBkZWZlcnJlZC5sZW5ndGg7IGkrKykge1xuXHRcdHZhciBbY2h1bmtJZHMsIGZuLCBwcmlvcml0eV0gPSBkZWZlcnJlZFtpXTtcblx0XHR2YXIgZnVsZmlsbGVkID0gdHJ1ZTtcblx0XHRmb3IgKHZhciBqID0gMDsgaiA8IGNodW5rSWRzLmxlbmd0aDsgaisrKSB7XG5cdFx0XHRpZiAoKHByaW9yaXR5ICYgMSA9PT0gMCB8fCBub3RGdWxmaWxsZWQgPj0gcHJpb3JpdHkpICYmIE9iamVjdC5rZXlzKF9fd2VicGFja19yZXF1aXJlX18uTykuZXZlcnkoKGtleSkgPT4gKF9fd2VicGFja19yZXF1aXJlX18uT1trZXldKGNodW5rSWRzW2pdKSkpKSB7XG5cdFx0XHRcdGNodW5rSWRzLnNwbGljZShqLS0sIDEpO1xuXHRcdFx0fSBlbHNlIHtcblx0XHRcdFx0ZnVsZmlsbGVkID0gZmFsc2U7XG5cdFx0XHRcdGlmKHByaW9yaXR5IDwgbm90RnVsZmlsbGVkKSBub3RGdWxmaWxsZWQgPSBwcmlvcml0eTtcblx0XHRcdH1cblx0XHR9XG5cdFx0aWYoZnVsZmlsbGVkKSB7XG5cdFx0XHRkZWZlcnJlZC5zcGxpY2UoaS0tLCAxKVxuXHRcdFx0dmFyIHIgPSBmbigpO1xuXHRcdFx0aWYgKHIgIT09IHVuZGVmaW5lZCkgcmVzdWx0ID0gcjtcblx0XHR9XG5cdH1cblx0cmV0dXJuIHJlc3VsdDtcbn07IiwiLy8gZGVmaW5lIGdldHRlciBmdW5jdGlvbnMgZm9yIGhhcm1vbnkgZXhwb3J0c1xuX193ZWJwYWNrX3JlcXVpcmVfXy5kID0gKGV4cG9ydHMsIGRlZmluaXRpb24pID0+IHtcblx0Zm9yKHZhciBrZXkgaW4gZGVmaW5pdGlvbikge1xuXHRcdGlmKF9fd2VicGFja19yZXF1aXJlX18ubyhkZWZpbml0aW9uLCBrZXkpICYmICFfX3dlYnBhY2tfcmVxdWlyZV9fLm8oZXhwb3J0cywga2V5KSkge1xuXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIGtleSwgeyBlbnVtZXJhYmxlOiB0cnVlLCBnZXQ6IGRlZmluaXRpb25ba2V5XSB9KTtcblx0XHR9XG5cdH1cbn07IiwiX193ZWJwYWNrX3JlcXVpcmVfXy5mID0ge307XG4vLyBUaGlzIGZpbGUgY29udGFpbnMgb25seSB0aGUgZW50cnkgY2h1bmsuXG4vLyBUaGUgY2h1bmsgbG9hZGluZyBmdW5jdGlvbiBmb3IgYWRkaXRpb25hbCBjaHVua3Ncbl9fd2VicGFja19yZXF1aXJlX18uZSA9IChjaHVua0lkKSA9PiB7XG5cdHJldHVybiBQcm9taXNlLmFsbChPYmplY3Qua2V5cyhfX3dlYnBhY2tfcmVxdWlyZV9fLmYpLnJlZHVjZSgocHJvbWlzZXMsIGtleSkgPT4ge1xuXHRcdF9fd2VicGFja19yZXF1aXJlX18uZltrZXldKGNodW5rSWQsIHByb21pc2VzKTtcblx0XHRyZXR1cm4gcHJvbWlzZXM7XG5cdH0sIFtdKSk7XG59OyIsIi8vIFRoaXMgZnVuY3Rpb24gYWxsb3cgdG8gcmVmZXJlbmNlIGFzeW5jIGNodW5rcyBhbmQgc2libGluZyBjaHVua3MgZm9yIHRoZSBlbnRyeXBvaW50XG5fX3dlYnBhY2tfcmVxdWlyZV9fLnUgPSAoY2h1bmtJZCkgPT4ge1xuXHQvLyByZXR1cm4gdXJsIGZvciBmaWxlbmFtZXMgYmFzZWQgb24gdGVtcGxhdGVcblx0cmV0dXJuIFwiXCIgKyBjaHVua0lkICsgXCIuanVweXRlci12aWV3ZXIuanNcIjtcbn07IiwiX193ZWJwYWNrX3JlcXVpcmVfXy5nID0gKGZ1bmN0aW9uKCkge1xuXHRpZiAodHlwZW9mIGdsb2JhbFRoaXMgPT09ICdvYmplY3QnKSByZXR1cm4gZ2xvYmFsVGhpcztcblx0dHJ5IHtcblx0XHRyZXR1cm4gdGhpcyB8fCBuZXcgRnVuY3Rpb24oJ3JldHVybiB0aGlzJykoKTtcblx0fSBjYXRjaCAoZSkge1xuXHRcdGlmICh0eXBlb2Ygd2luZG93ID09PSAnb2JqZWN0JykgcmV0dXJuIHdpbmRvdztcblx0fVxufSkoKTsiLCJfX3dlYnBhY2tfcmVxdWlyZV9fLm8gPSAob2JqLCBwcm9wKSA9PiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iaiwgcHJvcCkpIiwiX193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCIvc3RhdGljL2p1cHl0ZXJfdmlld2VyL1wiOyIsIi8vIG5vIGJhc2VVUklcblxuLy8gb2JqZWN0IHRvIHN0b3JlIGxvYWRlZCBjaHVua3Ncbi8vIFwiMVwiIG1lYW5zIFwiYWxyZWFkeSBsb2FkZWRcIlxudmFyIGluc3RhbGxlZENodW5rcyA9IHtcblx0MzU5NjogMVxufTtcblxuLy8gaW1wb3J0U2NyaXB0cyBjaHVuayBsb2FkaW5nXG52YXIgaW5zdGFsbENodW5rID0gKGRhdGEpID0+IHtcblx0dmFyIFtjaHVua0lkcywgbW9yZU1vZHVsZXMsIHJ1bnRpbWVdID0gZGF0YTtcblx0Zm9yKHZhciBtb2R1bGVJZCBpbiBtb3JlTW9kdWxlcykge1xuXHRcdGlmKF9fd2VicGFja19yZXF1aXJlX18ubyhtb3JlTW9kdWxlcywgbW9kdWxlSWQpKSB7XG5cdFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLm1bbW9kdWxlSWRdID0gbW9yZU1vZHVsZXNbbW9kdWxlSWRdO1xuXHRcdH1cblx0fVxuXHRpZihydW50aW1lKSBydW50aW1lKF9fd2VicGFja19yZXF1aXJlX18pO1xuXHR3aGlsZShjaHVua0lkcy5sZW5ndGgpXG5cdFx0aW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRzLnBvcCgpXSA9IDE7XG5cdHBhcmVudENodW5rTG9hZGluZ0Z1bmN0aW9uKGRhdGEpO1xufTtcbl9fd2VicGFja19yZXF1aXJlX18uZi5pID0gKGNodW5rSWQsIHByb21pc2VzKSA9PiB7XG5cdC8vIFwiMVwiIGlzIHRoZSBzaWduYWwgZm9yIFwiYWxyZWFkeSBsb2FkZWRcIlxuXHRpZighaW5zdGFsbGVkQ2h1bmtzW2NodW5rSWRdKSB7XG5cdFx0aWYodHJ1ZSkgeyAvLyBhbGwgY2h1bmtzIGhhdmUgSlNcblx0XHRcdGltcG9ydFNjcmlwdHMoX193ZWJwYWNrX3JlcXVpcmVfXy5wICsgX193ZWJwYWNrX3JlcXVpcmVfXy51KGNodW5rSWQpKTtcblx0XHR9XG5cdH1cbn07XG5cbnZhciBjaHVua0xvYWRpbmdHbG9iYWwgPSBzZWxmW1wid2VicGFja0NodW5rX2RhdGFsYXllcl9qdXB5dGVyX3ZpZXdlclwiXSA9IHNlbGZbXCJ3ZWJwYWNrQ2h1bmtfZGF0YWxheWVyX2p1cHl0ZXJfdmlld2VyXCJdIHx8IFtdO1xudmFyIHBhcmVudENodW5rTG9hZGluZ0Z1bmN0aW9uID0gY2h1bmtMb2FkaW5nR2xvYmFsLnB1c2guYmluZChjaHVua0xvYWRpbmdHbG9iYWwpO1xuY2h1bmtMb2FkaW5nR2xvYmFsLnB1c2ggPSBpbnN0YWxsQ2h1bms7XG5cbi8vIG5vIEhNUlxuXG4vLyBubyBITVIgbWFuaWZlc3QiLCJ2YXIgbmV4dCA9IF9fd2VicGFja19yZXF1aXJlX18ueDtcbl9fd2VicGFja19yZXF1aXJlX18ueCA9ICgpID0+IHtcblx0cmV0dXJuIF9fd2VicGFja19yZXF1aXJlX18uZSg3MTc5KS50aGVuKG5leHQpO1xufTsiLCIiLCIvLyBydW4gc3RhcnR1cFxudmFyIF9fd2VicGFja19leHBvcnRzX18gPSBfX3dlYnBhY2tfcmVxdWlyZV9fLngoKTtcbiIsIiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==