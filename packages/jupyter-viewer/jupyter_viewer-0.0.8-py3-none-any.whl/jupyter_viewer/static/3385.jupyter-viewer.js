"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3385],{

/***/ 184:
/***/ ((__unused_webpack_module, exports) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.VERSION = void 0;
exports.VERSION = '3.2.2';

/***/ }),

/***/ 2730:
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {



var __extends = this && this.__extends || function () {
  var extendStatics = function (d, b) {
    extendStatics = Object.setPrototypeOf || {
      __proto__: []
    } instanceof Array && function (d, b) {
      d.__proto__ = b;
    } || function (d, b) {
      for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p];
    };
    return extendStatics(d, b);
  };
  return function (d, b) {
    if (typeof b !== "function" && b !== null) throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
    extendStatics(d, b);
    function __() {
      this.constructor = d;
    }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
  };
}();
var __values = this && this.__values || function (o) {
  var s = typeof Symbol === "function" && Symbol.iterator,
    m = s && o[s],
    i = 0;
  if (m) return m.call(o);
  if (o && typeof o.length === "number") return {
    next: function () {
      if (o && i >= o.length) o = void 0;
      return {
        value: o && o[i++],
        done: !o
      };
    }
  };
  throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};
Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.HandlerList = void 0;
var PrioritizedList_js_1 = __webpack_require__(47144);
var HandlerList = function (_super) {
  __extends(HandlerList, _super);
  function HandlerList() {
    return _super !== null && _super.apply(this, arguments) || this;
  }
  HandlerList.prototype.register = function (handler) {
    return this.add(handler, handler.priority);
  };
  HandlerList.prototype.unregister = function (handler) {
    this.remove(handler);
  };
  HandlerList.prototype.handlesDocument = function (document) {
    var e_1, _a;
    try {
      for (var _b = __values(this), _c = _b.next(); !_c.done; _c = _b.next()) {
        var item = _c.value;
        var handler = item.item;
        if (handler.handlesDocument(document)) {
          return handler;
        }
      }
    } catch (e_1_1) {
      e_1 = {
        error: e_1_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_1) throw e_1.error;
      }
    }
    throw new Error("Can't find handler for document");
  };
  HandlerList.prototype.document = function (document, options) {
    if (options === void 0) {
      options = null;
    }
    return this.handlesDocument(document).create(document, options);
  };
  return HandlerList;
}(PrioritizedList_js_1.PrioritizedList);
exports.HandlerList = HandlerList;

/***/ }),

/***/ 63385:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.mathjax = void 0;
var version_js_1 = __webpack_require__(184);
var HandlerList_js_1 = __webpack_require__(2730);
var Retries_js_1 = __webpack_require__(69992);
exports.mathjax = {
  version: version_js_1.VERSION,
  handlers: new HandlerList_js_1.HandlerList(),
  document: function (document, options) {
    return exports.mathjax.handlers.document(document, options);
  },
  handleRetriesFor: Retries_js_1.handleRetriesFor,
  retryAfter: Retries_js_1.retryAfter,
  asyncLoad: null
};

/***/ }),

/***/ 47144:
/***/ ((__unused_webpack_module, exports) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.PrioritizedList = void 0;
var PrioritizedList = function () {
  function PrioritizedList() {
    this.items = [];
    this.items = [];
  }
  PrioritizedList.prototype[Symbol.iterator] = function () {
    var i = 0;
    var items = this.items;
    return {
      next: function () {
        return {
          value: items[i++],
          done: i > items.length
        };
      }
    };
  };
  PrioritizedList.prototype.add = function (item, priority) {
    if (priority === void 0) {
      priority = PrioritizedList.DEFAULTPRIORITY;
    }
    var i = this.items.length;
    do {
      i--;
    } while (i >= 0 && priority < this.items[i].priority);
    this.items.splice(i + 1, 0, {
      item: item,
      priority: priority
    });
    return item;
  };
  PrioritizedList.prototype.remove = function (item) {
    var i = this.items.length;
    do {
      i--;
    } while (i >= 0 && this.items[i].item !== item);
    if (i >= 0) {
      this.items.splice(i, 1);
    }
  };
  PrioritizedList.DEFAULTPRIORITY = 5;
  return PrioritizedList;
}();
exports.PrioritizedList = PrioritizedList;

/***/ }),

/***/ 69992:
/***/ ((__unused_webpack_module, exports) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.retryAfter = exports.handleRetriesFor = void 0;
function handleRetriesFor(code) {
  return new Promise(function run(ok, fail) {
    try {
      ok(code());
    } catch (err) {
      if (err.retry && err.retry instanceof Promise) {
        err.retry.then(function () {
          return run(ok, fail);
        }).catch(function (perr) {
          return fail(perr);
        });
      } else if (err.restart && err.restart.isCallback) {
        MathJax.Callback.After(function () {
          return run(ok, fail);
        }, err.restart);
      } else {
        fail(err);
      }
    }
  });
}
exports.handleRetriesFor = handleRetriesFor;
function retryAfter(promise) {
  var err = new Error('MathJax retry');
  err.retry = promise;
  throw err;
}
exports.retryAfter = retryAfter;

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzM4NS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ05BO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUNyRkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUNsQkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7OztBQ2pEQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL2NvbXBvbmVudHMvdmVyc2lvbi5qcyIsIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL21hdGhqYXgtZnVsbC9qcy9jb3JlL0hhbmRsZXJMaXN0LmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvbWF0aGpheC1mdWxsL2pzL21hdGhqYXguanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvdXRpbC9Qcmlvcml0aXplZExpc3QuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvdXRpbC9SZXRyaWVzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIlwidXNlIHN0cmljdFwiO1xuXG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5WRVJTSU9OID0gdm9pZCAwO1xuZXhwb3J0cy5WRVJTSU9OID0gJzMuMi4yJzsiLCJcInVzZSBzdHJpY3RcIjtcblxudmFyIF9fZXh0ZW5kcyA9IHRoaXMgJiYgdGhpcy5fX2V4dGVuZHMgfHwgZnVuY3Rpb24gKCkge1xuICB2YXIgZXh0ZW5kU3RhdGljcyA9IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgZXh0ZW5kU3RhdGljcyA9IE9iamVjdC5zZXRQcm90b3R5cGVPZiB8fCB7XG4gICAgICBfX3Byb3RvX186IFtdXG4gICAgfSBpbnN0YW5jZW9mIEFycmF5ICYmIGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBkLl9fcHJvdG9fXyA9IGI7XG4gICAgfSB8fCBmdW5jdGlvbiAoZCwgYikge1xuICAgICAgZm9yICh2YXIgcCBpbiBiKSBpZiAoT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKGIsIHApKSBkW3BdID0gYltwXTtcbiAgICB9O1xuICAgIHJldHVybiBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICB9O1xuICByZXR1cm4gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBpZiAodHlwZW9mIGIgIT09IFwiZnVuY3Rpb25cIiAmJiBiICE9PSBudWxsKSB0aHJvdyBuZXcgVHlwZUVycm9yKFwiQ2xhc3MgZXh0ZW5kcyB2YWx1ZSBcIiArIFN0cmluZyhiKSArIFwiIGlzIG5vdCBhIGNvbnN0cnVjdG9yIG9yIG51bGxcIik7XG4gICAgZXh0ZW5kU3RhdGljcyhkLCBiKTtcbiAgICBmdW5jdGlvbiBfXygpIHtcbiAgICAgIHRoaXMuY29uc3RydWN0b3IgPSBkO1xuICAgIH1cbiAgICBkLnByb3RvdHlwZSA9IGIgPT09IG51bGwgPyBPYmplY3QuY3JlYXRlKGIpIDogKF9fLnByb3RvdHlwZSA9IGIucHJvdG90eXBlLCBuZXcgX18oKSk7XG4gIH07XG59KCk7XG52YXIgX192YWx1ZXMgPSB0aGlzICYmIHRoaXMuX192YWx1ZXMgfHwgZnVuY3Rpb24gKG8pIHtcbiAgdmFyIHMgPSB0eXBlb2YgU3ltYm9sID09PSBcImZ1bmN0aW9uXCIgJiYgU3ltYm9sLml0ZXJhdG9yLFxuICAgIG0gPSBzICYmIG9bc10sXG4gICAgaSA9IDA7XG4gIGlmIChtKSByZXR1cm4gbS5jYWxsKG8pO1xuICBpZiAobyAmJiB0eXBlb2Ygby5sZW5ndGggPT09IFwibnVtYmVyXCIpIHJldHVybiB7XG4gICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgaWYgKG8gJiYgaSA+PSBvLmxlbmd0aCkgbyA9IHZvaWQgMDtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHZhbHVlOiBvICYmIG9baSsrXSxcbiAgICAgICAgZG9uZTogIW9cbiAgICAgIH07XG4gICAgfVxuICB9O1xuICB0aHJvdyBuZXcgVHlwZUVycm9yKHMgPyBcIk9iamVjdCBpcyBub3QgaXRlcmFibGUuXCIgOiBcIlN5bWJvbC5pdGVyYXRvciBpcyBub3QgZGVmaW5lZC5cIik7XG59O1xuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMuSGFuZGxlckxpc3QgPSB2b2lkIDA7XG52YXIgUHJpb3JpdGl6ZWRMaXN0X2pzXzEgPSByZXF1aXJlKFwiLi4vdXRpbC9Qcmlvcml0aXplZExpc3QuanNcIik7XG52YXIgSGFuZGxlckxpc3QgPSBmdW5jdGlvbiAoX3N1cGVyKSB7XG4gIF9fZXh0ZW5kcyhIYW5kbGVyTGlzdCwgX3N1cGVyKTtcbiAgZnVuY3Rpb24gSGFuZGxlckxpc3QoKSB7XG4gICAgcmV0dXJuIF9zdXBlciAhPT0gbnVsbCAmJiBfc3VwZXIuYXBwbHkodGhpcywgYXJndW1lbnRzKSB8fCB0aGlzO1xuICB9XG4gIEhhbmRsZXJMaXN0LnByb3RvdHlwZS5yZWdpc3RlciA9IGZ1bmN0aW9uIChoYW5kbGVyKSB7XG4gICAgcmV0dXJuIHRoaXMuYWRkKGhhbmRsZXIsIGhhbmRsZXIucHJpb3JpdHkpO1xuICB9O1xuICBIYW5kbGVyTGlzdC5wcm90b3R5cGUudW5yZWdpc3RlciA9IGZ1bmN0aW9uIChoYW5kbGVyKSB7XG4gICAgdGhpcy5yZW1vdmUoaGFuZGxlcik7XG4gIH07XG4gIEhhbmRsZXJMaXN0LnByb3RvdHlwZS5oYW5kbGVzRG9jdW1lbnQgPSBmdW5jdGlvbiAoZG9jdW1lbnQpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB0cnkge1xuICAgICAgZm9yICh2YXIgX2IgPSBfX3ZhbHVlcyh0aGlzKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgICB2YXIgaXRlbSA9IF9jLnZhbHVlO1xuICAgICAgICB2YXIgaGFuZGxlciA9IGl0ZW0uaXRlbTtcbiAgICAgICAgaWYgKGhhbmRsZXIuaGFuZGxlc0RvY3VtZW50KGRvY3VtZW50KSkge1xuICAgICAgICAgIHJldHVybiBoYW5kbGVyO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZV8xXzEpIHtcbiAgICAgIGVfMSA9IHtcbiAgICAgICAgZXJyb3I6IGVfMV8xXG4gICAgICB9O1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0cnkge1xuICAgICAgICBpZiAoX2MgJiYgIV9jLmRvbmUgJiYgKF9hID0gX2IucmV0dXJuKSkgX2EuY2FsbChfYik7XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICBpZiAoZV8xKSB0aHJvdyBlXzEuZXJyb3I7XG4gICAgICB9XG4gICAgfVxuICAgIHRocm93IG5ldyBFcnJvcihcIkNhbid0IGZpbmQgaGFuZGxlciBmb3IgZG9jdW1lbnRcIik7XG4gIH07XG4gIEhhbmRsZXJMaXN0LnByb3RvdHlwZS5kb2N1bWVudCA9IGZ1bmN0aW9uIChkb2N1bWVudCwgb3B0aW9ucykge1xuICAgIGlmIChvcHRpb25zID09PSB2b2lkIDApIHtcbiAgICAgIG9wdGlvbnMgPSBudWxsO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5oYW5kbGVzRG9jdW1lbnQoZG9jdW1lbnQpLmNyZWF0ZShkb2N1bWVudCwgb3B0aW9ucyk7XG4gIH07XG4gIHJldHVybiBIYW5kbGVyTGlzdDtcbn0oUHJpb3JpdGl6ZWRMaXN0X2pzXzEuUHJpb3JpdGl6ZWRMaXN0KTtcbmV4cG9ydHMuSGFuZGxlckxpc3QgPSBIYW5kbGVyTGlzdDsiLCJcInVzZSBzdHJpY3RcIjtcblxuT2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIFwiX19lc01vZHVsZVwiLCB7XG4gIHZhbHVlOiB0cnVlXG59KTtcbmV4cG9ydHMubWF0aGpheCA9IHZvaWQgMDtcbnZhciB2ZXJzaW9uX2pzXzEgPSByZXF1aXJlKFwiLi9jb21wb25lbnRzL3ZlcnNpb24uanNcIik7XG52YXIgSGFuZGxlckxpc3RfanNfMSA9IHJlcXVpcmUoXCIuL2NvcmUvSGFuZGxlckxpc3QuanNcIik7XG52YXIgUmV0cmllc19qc18xID0gcmVxdWlyZShcIi4vdXRpbC9SZXRyaWVzLmpzXCIpO1xuZXhwb3J0cy5tYXRoamF4ID0ge1xuICB2ZXJzaW9uOiB2ZXJzaW9uX2pzXzEuVkVSU0lPTixcbiAgaGFuZGxlcnM6IG5ldyBIYW5kbGVyTGlzdF9qc18xLkhhbmRsZXJMaXN0KCksXG4gIGRvY3VtZW50OiBmdW5jdGlvbiAoZG9jdW1lbnQsIG9wdGlvbnMpIHtcbiAgICByZXR1cm4gZXhwb3J0cy5tYXRoamF4LmhhbmRsZXJzLmRvY3VtZW50KGRvY3VtZW50LCBvcHRpb25zKTtcbiAgfSxcbiAgaGFuZGxlUmV0cmllc0ZvcjogUmV0cmllc19qc18xLmhhbmRsZVJldHJpZXNGb3IsXG4gIHJldHJ5QWZ0ZXI6IFJldHJpZXNfanNfMS5yZXRyeUFmdGVyLFxuICBhc3luY0xvYWQ6IG51bGxcbn07IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLlByaW9yaXRpemVkTGlzdCA9IHZvaWQgMDtcbnZhciBQcmlvcml0aXplZExpc3QgPSBmdW5jdGlvbiAoKSB7XG4gIGZ1bmN0aW9uIFByaW9yaXRpemVkTGlzdCgpIHtcbiAgICB0aGlzLml0ZW1zID0gW107XG4gICAgdGhpcy5pdGVtcyA9IFtdO1xuICB9XG4gIFByaW9yaXRpemVkTGlzdC5wcm90b3R5cGVbU3ltYm9sLml0ZXJhdG9yXSA9IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgaSA9IDA7XG4gICAgdmFyIGl0ZW1zID0gdGhpcy5pdGVtcztcbiAgICByZXR1cm4ge1xuICAgICAgbmV4dDogZnVuY3Rpb24gKCkge1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIHZhbHVlOiBpdGVtc1tpKytdLFxuICAgICAgICAgIGRvbmU6IGkgPiBpdGVtcy5sZW5ndGhcbiAgICAgICAgfTtcbiAgICAgIH1cbiAgICB9O1xuICB9O1xuICBQcmlvcml0aXplZExpc3QucHJvdG90eXBlLmFkZCA9IGZ1bmN0aW9uIChpdGVtLCBwcmlvcml0eSkge1xuICAgIGlmIChwcmlvcml0eSA9PT0gdm9pZCAwKSB7XG4gICAgICBwcmlvcml0eSA9IFByaW9yaXRpemVkTGlzdC5ERUZBVUxUUFJJT1JJVFk7XG4gICAgfVxuICAgIHZhciBpID0gdGhpcy5pdGVtcy5sZW5ndGg7XG4gICAgZG8ge1xuICAgICAgaS0tO1xuICAgIH0gd2hpbGUgKGkgPj0gMCAmJiBwcmlvcml0eSA8IHRoaXMuaXRlbXNbaV0ucHJpb3JpdHkpO1xuICAgIHRoaXMuaXRlbXMuc3BsaWNlKGkgKyAxLCAwLCB7XG4gICAgICBpdGVtOiBpdGVtLFxuICAgICAgcHJpb3JpdHk6IHByaW9yaXR5XG4gICAgfSk7XG4gICAgcmV0dXJuIGl0ZW07XG4gIH07XG4gIFByaW9yaXRpemVkTGlzdC5wcm90b3R5cGUucmVtb3ZlID0gZnVuY3Rpb24gKGl0ZW0pIHtcbiAgICB2YXIgaSA9IHRoaXMuaXRlbXMubGVuZ3RoO1xuICAgIGRvIHtcbiAgICAgIGktLTtcbiAgICB9IHdoaWxlIChpID49IDAgJiYgdGhpcy5pdGVtc1tpXS5pdGVtICE9PSBpdGVtKTtcbiAgICBpZiAoaSA+PSAwKSB7XG4gICAgICB0aGlzLml0ZW1zLnNwbGljZShpLCAxKTtcbiAgICB9XG4gIH07XG4gIFByaW9yaXRpemVkTGlzdC5ERUZBVUxUUFJJT1JJVFkgPSA1O1xuICByZXR1cm4gUHJpb3JpdGl6ZWRMaXN0O1xufSgpO1xuZXhwb3J0cy5Qcmlvcml0aXplZExpc3QgPSBQcmlvcml0aXplZExpc3Q7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbk9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBcIl9fZXNNb2R1bGVcIiwge1xuICB2YWx1ZTogdHJ1ZVxufSk7XG5leHBvcnRzLnJldHJ5QWZ0ZXIgPSBleHBvcnRzLmhhbmRsZVJldHJpZXNGb3IgPSB2b2lkIDA7XG5mdW5jdGlvbiBoYW5kbGVSZXRyaWVzRm9yKGNvZGUpIHtcbiAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uIHJ1bihvaywgZmFpbCkge1xuICAgIHRyeSB7XG4gICAgICBvayhjb2RlKCkpO1xuICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgaWYgKGVyci5yZXRyeSAmJiBlcnIucmV0cnkgaW5zdGFuY2VvZiBQcm9taXNlKSB7XG4gICAgICAgIGVyci5yZXRyeS50aGVuKGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICByZXR1cm4gcnVuKG9rLCBmYWlsKTtcbiAgICAgICAgfSkuY2F0Y2goZnVuY3Rpb24gKHBlcnIpIHtcbiAgICAgICAgICByZXR1cm4gZmFpbChwZXJyKTtcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2UgaWYgKGVyci5yZXN0YXJ0ICYmIGVyci5yZXN0YXJ0LmlzQ2FsbGJhY2spIHtcbiAgICAgICAgTWF0aEpheC5DYWxsYmFjay5BZnRlcihmdW5jdGlvbiAoKSB7XG4gICAgICAgICAgcmV0dXJuIHJ1bihvaywgZmFpbCk7XG4gICAgICAgIH0sIGVyci5yZXN0YXJ0KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGZhaWwoZXJyKTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xufVxuZXhwb3J0cy5oYW5kbGVSZXRyaWVzRm9yID0gaGFuZGxlUmV0cmllc0ZvcjtcbmZ1bmN0aW9uIHJldHJ5QWZ0ZXIocHJvbWlzZSkge1xuICB2YXIgZXJyID0gbmV3IEVycm9yKCdNYXRoSmF4IHJldHJ5Jyk7XG4gIGVyci5yZXRyeSA9IHByb21pc2U7XG4gIHRocm93IGVycjtcbn1cbmV4cG9ydHMucmV0cnlBZnRlciA9IHJldHJ5QWZ0ZXI7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9