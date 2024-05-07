"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[4637],{

/***/ 58691:
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
exports.HTMLAdaptor = void 0;
var DOMAdaptor_js_1 = __webpack_require__(40979);
var HTMLAdaptor = function (_super) {
  __extends(HTMLAdaptor, _super);
  function HTMLAdaptor(window) {
    var _this = _super.call(this, window.document) || this;
    _this.window = window;
    _this.parser = new window.DOMParser();
    return _this;
  }
  HTMLAdaptor.prototype.parse = function (text, format) {
    if (format === void 0) {
      format = 'text/html';
    }
    return this.parser.parseFromString(text, format);
  };
  HTMLAdaptor.prototype.create = function (kind, ns) {
    return ns ? this.document.createElementNS(ns, kind) : this.document.createElement(kind);
  };
  HTMLAdaptor.prototype.text = function (text) {
    return this.document.createTextNode(text);
  };
  HTMLAdaptor.prototype.head = function (doc) {
    return doc.head || doc;
  };
  HTMLAdaptor.prototype.body = function (doc) {
    return doc.body || doc;
  };
  HTMLAdaptor.prototype.root = function (doc) {
    return doc.documentElement || doc;
  };
  HTMLAdaptor.prototype.doctype = function (doc) {
    return doc.doctype ? "<!DOCTYPE ".concat(doc.doctype.name, ">") : '';
  };
  HTMLAdaptor.prototype.tags = function (node, name, ns) {
    if (ns === void 0) {
      ns = null;
    }
    var nodes = ns ? node.getElementsByTagNameNS(ns, name) : node.getElementsByTagName(name);
    return Array.from(nodes);
  };
  HTMLAdaptor.prototype.getElements = function (nodes, _document) {
    var e_1, _a;
    var containers = [];
    try {
      for (var nodes_1 = __values(nodes), nodes_1_1 = nodes_1.next(); !nodes_1_1.done; nodes_1_1 = nodes_1.next()) {
        var node = nodes_1_1.value;
        if (typeof node === 'string') {
          containers = containers.concat(Array.from(this.document.querySelectorAll(node)));
        } else if (Array.isArray(node)) {
          containers = containers.concat(Array.from(node));
        } else if (node instanceof this.window.NodeList || node instanceof this.window.HTMLCollection) {
          containers = containers.concat(Array.from(node));
        } else {
          containers.push(node);
        }
      }
    } catch (e_1_1) {
      e_1 = {
        error: e_1_1
      };
    } finally {
      try {
        if (nodes_1_1 && !nodes_1_1.done && (_a = nodes_1.return)) _a.call(nodes_1);
      } finally {
        if (e_1) throw e_1.error;
      }
    }
    return containers;
  };
  HTMLAdaptor.prototype.contains = function (container, node) {
    return container.contains(node);
  };
  HTMLAdaptor.prototype.parent = function (node) {
    return node.parentNode;
  };
  HTMLAdaptor.prototype.append = function (node, child) {
    return node.appendChild(child);
  };
  HTMLAdaptor.prototype.insert = function (nchild, ochild) {
    return this.parent(ochild).insertBefore(nchild, ochild);
  };
  HTMLAdaptor.prototype.remove = function (child) {
    return this.parent(child).removeChild(child);
  };
  HTMLAdaptor.prototype.replace = function (nnode, onode) {
    return this.parent(onode).replaceChild(nnode, onode);
  };
  HTMLAdaptor.prototype.clone = function (node) {
    return node.cloneNode(true);
  };
  HTMLAdaptor.prototype.split = function (node, n) {
    return node.splitText(n);
  };
  HTMLAdaptor.prototype.next = function (node) {
    return node.nextSibling;
  };
  HTMLAdaptor.prototype.previous = function (node) {
    return node.previousSibling;
  };
  HTMLAdaptor.prototype.firstChild = function (node) {
    return node.firstChild;
  };
  HTMLAdaptor.prototype.lastChild = function (node) {
    return node.lastChild;
  };
  HTMLAdaptor.prototype.childNodes = function (node) {
    return Array.from(node.childNodes);
  };
  HTMLAdaptor.prototype.childNode = function (node, i) {
    return node.childNodes[i];
  };
  HTMLAdaptor.prototype.kind = function (node) {
    var n = node.nodeType;
    return n === 1 || n === 3 || n === 8 ? node.nodeName.toLowerCase() : '';
  };
  HTMLAdaptor.prototype.value = function (node) {
    return node.nodeValue || '';
  };
  HTMLAdaptor.prototype.textContent = function (node) {
    return node.textContent;
  };
  HTMLAdaptor.prototype.innerHTML = function (node) {
    return node.innerHTML;
  };
  HTMLAdaptor.prototype.outerHTML = function (node) {
    return node.outerHTML;
  };
  HTMLAdaptor.prototype.serializeXML = function (node) {
    var serializer = new this.window.XMLSerializer();
    return serializer.serializeToString(node);
  };
  HTMLAdaptor.prototype.setAttribute = function (node, name, value, ns) {
    if (ns === void 0) {
      ns = null;
    }
    if (!ns) {
      return node.setAttribute(name, value);
    }
    name = ns.replace(/.*\//, '') + ':' + name.replace(/^.*:/, '');
    return node.setAttributeNS(ns, name, value);
  };
  HTMLAdaptor.prototype.getAttribute = function (node, name) {
    return node.getAttribute(name);
  };
  HTMLAdaptor.prototype.removeAttribute = function (node, name) {
    return node.removeAttribute(name);
  };
  HTMLAdaptor.prototype.hasAttribute = function (node, name) {
    return node.hasAttribute(name);
  };
  HTMLAdaptor.prototype.allAttributes = function (node) {
    return Array.from(node.attributes).map(function (x) {
      return {
        name: x.name,
        value: x.value
      };
    });
  };
  HTMLAdaptor.prototype.addClass = function (node, name) {
    if (node.classList) {
      node.classList.add(name);
    } else {
      node.className = (node.className + ' ' + name).trim();
    }
  };
  HTMLAdaptor.prototype.removeClass = function (node, name) {
    if (node.classList) {
      node.classList.remove(name);
    } else {
      node.className = node.className.split(/ /).filter(function (c) {
        return c !== name;
      }).join(' ');
    }
  };
  HTMLAdaptor.prototype.hasClass = function (node, name) {
    if (node.classList) {
      return node.classList.contains(name);
    }
    return node.className.split(/ /).indexOf(name) >= 0;
  };
  HTMLAdaptor.prototype.setStyle = function (node, name, value) {
    node.style[name] = value;
  };
  HTMLAdaptor.prototype.getStyle = function (node, name) {
    return node.style[name];
  };
  HTMLAdaptor.prototype.allStyles = function (node) {
    return node.style.cssText;
  };
  HTMLAdaptor.prototype.insertRules = function (node, rules) {
    var e_2, _a;
    try {
      for (var _b = __values(rules.reverse()), _c = _b.next(); !_c.done; _c = _b.next()) {
        var rule = _c.value;
        try {
          node.sheet.insertRule(rule, 0);
        } catch (e) {
          console.warn("MathJax: can't insert css rule '".concat(rule, "': ").concat(e.message));
        }
      }
    } catch (e_2_1) {
      e_2 = {
        error: e_2_1
      };
    } finally {
      try {
        if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
      } finally {
        if (e_2) throw e_2.error;
      }
    }
  };
  HTMLAdaptor.prototype.fontSize = function (node) {
    var style = this.window.getComputedStyle(node);
    return parseFloat(style.fontSize);
  };
  HTMLAdaptor.prototype.fontFamily = function (node) {
    var style = this.window.getComputedStyle(node);
    return style.fontFamily || '';
  };
  HTMLAdaptor.prototype.nodeSize = function (node, em, local) {
    if (em === void 0) {
      em = 1;
    }
    if (local === void 0) {
      local = false;
    }
    if (local && node.getBBox) {
      var _a = node.getBBox(),
        width = _a.width,
        height = _a.height;
      return [width / em, height / em];
    }
    return [node.offsetWidth / em, node.offsetHeight / em];
  };
  HTMLAdaptor.prototype.nodeBBox = function (node) {
    var _a = node.getBoundingClientRect(),
      left = _a.left,
      right = _a.right,
      top = _a.top,
      bottom = _a.bottom;
    return {
      left: left,
      right: right,
      top: top,
      bottom: bottom
    };
  };
  return HTMLAdaptor;
}(DOMAdaptor_js_1.AbstractDOMAdaptor);
exports.HTMLAdaptor = HTMLAdaptor;

/***/ }),

/***/ 12973:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.browserAdaptor = void 0;
var HTMLAdaptor_js_1 = __webpack_require__(58691);
function browserAdaptor() {
  return new HTMLAdaptor_js_1.HTMLAdaptor(window);
}
exports.browserAdaptor = browserAdaptor;

/***/ }),

/***/ 40979:
/***/ (function(__unused_webpack_module, exports) {



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
exports.AbstractDOMAdaptor = void 0;
var AbstractDOMAdaptor = function () {
  function AbstractDOMAdaptor(document) {
    if (document === void 0) {
      document = null;
    }
    this.document = document;
  }
  AbstractDOMAdaptor.prototype.node = function (kind, def, children, ns) {
    var e_1, _a;
    if (def === void 0) {
      def = {};
    }
    if (children === void 0) {
      children = [];
    }
    var node = this.create(kind, ns);
    this.setAttributes(node, def);
    try {
      for (var children_1 = __values(children), children_1_1 = children_1.next(); !children_1_1.done; children_1_1 = children_1.next()) {
        var child = children_1_1.value;
        this.append(node, child);
      }
    } catch (e_1_1) {
      e_1 = {
        error: e_1_1
      };
    } finally {
      try {
        if (children_1_1 && !children_1_1.done && (_a = children_1.return)) _a.call(children_1);
      } finally {
        if (e_1) throw e_1.error;
      }
    }
    return node;
  };
  AbstractDOMAdaptor.prototype.setAttributes = function (node, def) {
    var e_2, _a, e_3, _b, e_4, _c;
    if (def.style && typeof def.style !== 'string') {
      try {
        for (var _d = __values(Object.keys(def.style)), _e = _d.next(); !_e.done; _e = _d.next()) {
          var key = _e.value;
          this.setStyle(node, key.replace(/-([a-z])/g, function (_m, c) {
            return c.toUpperCase();
          }), def.style[key]);
        }
      } catch (e_2_1) {
        e_2 = {
          error: e_2_1
        };
      } finally {
        try {
          if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
        } finally {
          if (e_2) throw e_2.error;
        }
      }
    }
    if (def.properties) {
      try {
        for (var _f = __values(Object.keys(def.properties)), _g = _f.next(); !_g.done; _g = _f.next()) {
          var key = _g.value;
          node[key] = def.properties[key];
        }
      } catch (e_3_1) {
        e_3 = {
          error: e_3_1
        };
      } finally {
        try {
          if (_g && !_g.done && (_b = _f.return)) _b.call(_f);
        } finally {
          if (e_3) throw e_3.error;
        }
      }
    }
    try {
      for (var _h = __values(Object.keys(def)), _j = _h.next(); !_j.done; _j = _h.next()) {
        var key = _j.value;
        if ((key !== 'style' || typeof def.style === 'string') && key !== 'properties') {
          this.setAttribute(node, key, def[key]);
        }
      }
    } catch (e_4_1) {
      e_4 = {
        error: e_4_1
      };
    } finally {
      try {
        if (_j && !_j.done && (_c = _h.return)) _c.call(_h);
      } finally {
        if (e_4) throw e_4.error;
      }
    }
  };
  AbstractDOMAdaptor.prototype.replace = function (nnode, onode) {
    this.insert(nnode, onode);
    this.remove(onode);
    return onode;
  };
  AbstractDOMAdaptor.prototype.childNode = function (node, i) {
    return this.childNodes(node)[i];
  };
  AbstractDOMAdaptor.prototype.allClasses = function (node) {
    var classes = this.getAttribute(node, 'class');
    return !classes ? [] : classes.replace(/  +/g, ' ').replace(/^ /, '').replace(/ $/, '').split(/ /);
  };
  return AbstractDOMAdaptor;
}();
exports.AbstractDOMAdaptor = AbstractDOMAdaptor;

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNDYzNy5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOzs7Ozs7O0FDcFNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7QUNWQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvYWRhcHRvcnMvSFRNTEFkYXB0b3IuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvYWRhcHRvcnMvYnJvd3NlckFkYXB0b3IuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9tYXRoamF4LWZ1bGwvanMvY29yZS9ET01BZGFwdG9yLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIlwidXNlIHN0cmljdFwiO1xuXG52YXIgX19leHRlbmRzID0gdGhpcyAmJiB0aGlzLl9fZXh0ZW5kcyB8fCBmdW5jdGlvbiAoKSB7XG4gIHZhciBleHRlbmRTdGF0aWNzID0gZnVuY3Rpb24gKGQsIGIpIHtcbiAgICBleHRlbmRTdGF0aWNzID0gT2JqZWN0LnNldFByb3RvdHlwZU9mIHx8IHtcbiAgICAgIF9fcHJvdG9fXzogW11cbiAgICB9IGluc3RhbmNlb2YgQXJyYXkgJiYgZnVuY3Rpb24gKGQsIGIpIHtcbiAgICAgIGQuX19wcm90b19fID0gYjtcbiAgICB9IHx8IGZ1bmN0aW9uIChkLCBiKSB7XG4gICAgICBmb3IgKHZhciBwIGluIGIpIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwoYiwgcCkpIGRbcF0gPSBiW3BdO1xuICAgIH07XG4gICAgcmV0dXJuIGV4dGVuZFN0YXRpY3MoZCwgYik7XG4gIH07XG4gIHJldHVybiBmdW5jdGlvbiAoZCwgYikge1xuICAgIGlmICh0eXBlb2YgYiAhPT0gXCJmdW5jdGlvblwiICYmIGIgIT09IG51bGwpIHRocm93IG5ldyBUeXBlRXJyb3IoXCJDbGFzcyBleHRlbmRzIHZhbHVlIFwiICsgU3RyaW5nKGIpICsgXCIgaXMgbm90IGEgY29uc3RydWN0b3Igb3IgbnVsbFwiKTtcbiAgICBleHRlbmRTdGF0aWNzKGQsIGIpO1xuICAgIGZ1bmN0aW9uIF9fKCkge1xuICAgICAgdGhpcy5jb25zdHJ1Y3RvciA9IGQ7XG4gICAgfVxuICAgIGQucHJvdG90eXBlID0gYiA9PT0gbnVsbCA/IE9iamVjdC5jcmVhdGUoYikgOiAoX18ucHJvdG90eXBlID0gYi5wcm90b3R5cGUsIG5ldyBfXygpKTtcbiAgfTtcbn0oKTtcbnZhciBfX3ZhbHVlcyA9IHRoaXMgJiYgdGhpcy5fX3ZhbHVlcyB8fCBmdW5jdGlvbiAobykge1xuICB2YXIgcyA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBTeW1ib2wuaXRlcmF0b3IsXG4gICAgbSA9IHMgJiYgb1tzXSxcbiAgICBpID0gMDtcbiAgaWYgKG0pIHJldHVybiBtLmNhbGwobyk7XG4gIGlmIChvICYmIHR5cGVvZiBvLmxlbmd0aCA9PT0gXCJudW1iZXJcIikgcmV0dXJuIHtcbiAgICBuZXh0OiBmdW5jdGlvbiAoKSB7XG4gICAgICBpZiAobyAmJiBpID49IG8ubGVuZ3RoKSBvID0gdm9pZCAwO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdmFsdWU6IG8gJiYgb1tpKytdLFxuICAgICAgICBkb25lOiAhb1xuICAgICAgfTtcbiAgICB9XG4gIH07XG4gIHRocm93IG5ldyBUeXBlRXJyb3IocyA/IFwiT2JqZWN0IGlzIG5vdCBpdGVyYWJsZS5cIiA6IFwiU3ltYm9sLml0ZXJhdG9yIGlzIG5vdCBkZWZpbmVkLlwiKTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5IVE1MQWRhcHRvciA9IHZvaWQgMDtcbnZhciBET01BZGFwdG9yX2pzXzEgPSByZXF1aXJlKFwiLi4vY29yZS9ET01BZGFwdG9yLmpzXCIpO1xudmFyIEhUTUxBZGFwdG9yID0gZnVuY3Rpb24gKF9zdXBlcikge1xuICBfX2V4dGVuZHMoSFRNTEFkYXB0b3IsIF9zdXBlcik7XG4gIGZ1bmN0aW9uIEhUTUxBZGFwdG9yKHdpbmRvdykge1xuICAgIHZhciBfdGhpcyA9IF9zdXBlci5jYWxsKHRoaXMsIHdpbmRvdy5kb2N1bWVudCkgfHwgdGhpcztcbiAgICBfdGhpcy53aW5kb3cgPSB3aW5kb3c7XG4gICAgX3RoaXMucGFyc2VyID0gbmV3IHdpbmRvdy5ET01QYXJzZXIoKTtcbiAgICByZXR1cm4gX3RoaXM7XG4gIH1cbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnBhcnNlID0gZnVuY3Rpb24gKHRleHQsIGZvcm1hdCkge1xuICAgIGlmIChmb3JtYXQgPT09IHZvaWQgMCkge1xuICAgICAgZm9ybWF0ID0gJ3RleHQvaHRtbCc7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLnBhcnNlci5wYXJzZUZyb21TdHJpbmcodGV4dCwgZm9ybWF0KTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmNyZWF0ZSA9IGZ1bmN0aW9uIChraW5kLCBucykge1xuICAgIHJldHVybiBucyA/IHRoaXMuZG9jdW1lbnQuY3JlYXRlRWxlbWVudE5TKG5zLCBraW5kKSA6IHRoaXMuZG9jdW1lbnQuY3JlYXRlRWxlbWVudChraW5kKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnRleHQgPSBmdW5jdGlvbiAodGV4dCkge1xuICAgIHJldHVybiB0aGlzLmRvY3VtZW50LmNyZWF0ZVRleHROb2RlKHRleHQpO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuaGVhZCA9IGZ1bmN0aW9uIChkb2MpIHtcbiAgICByZXR1cm4gZG9jLmhlYWQgfHwgZG9jO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuYm9keSA9IGZ1bmN0aW9uIChkb2MpIHtcbiAgICByZXR1cm4gZG9jLmJvZHkgfHwgZG9jO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUucm9vdCA9IGZ1bmN0aW9uIChkb2MpIHtcbiAgICByZXR1cm4gZG9jLmRvY3VtZW50RWxlbWVudCB8fCBkb2M7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5kb2N0eXBlID0gZnVuY3Rpb24gKGRvYykge1xuICAgIHJldHVybiBkb2MuZG9jdHlwZSA/IFwiPCFET0NUWVBFIFwiLmNvbmNhdChkb2MuZG9jdHlwZS5uYW1lLCBcIj5cIikgOiAnJztcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnRhZ3MgPSBmdW5jdGlvbiAobm9kZSwgbmFtZSwgbnMpIHtcbiAgICBpZiAobnMgPT09IHZvaWQgMCkge1xuICAgICAgbnMgPSBudWxsO1xuICAgIH1cbiAgICB2YXIgbm9kZXMgPSBucyA/IG5vZGUuZ2V0RWxlbWVudHNCeVRhZ05hbWVOUyhucywgbmFtZSkgOiBub2RlLmdldEVsZW1lbnRzQnlUYWdOYW1lKG5hbWUpO1xuICAgIHJldHVybiBBcnJheS5mcm9tKG5vZGVzKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmdldEVsZW1lbnRzID0gZnVuY3Rpb24gKG5vZGVzLCBfZG9jdW1lbnQpIHtcbiAgICB2YXIgZV8xLCBfYTtcbiAgICB2YXIgY29udGFpbmVycyA9IFtdO1xuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBub2Rlc18xID0gX192YWx1ZXMobm9kZXMpLCBub2Rlc18xXzEgPSBub2Rlc18xLm5leHQoKTsgIW5vZGVzXzFfMS5kb25lOyBub2Rlc18xXzEgPSBub2Rlc18xLm5leHQoKSkge1xuICAgICAgICB2YXIgbm9kZSA9IG5vZGVzXzFfMS52YWx1ZTtcbiAgICAgICAgaWYgKHR5cGVvZiBub2RlID09PSAnc3RyaW5nJykge1xuICAgICAgICAgIGNvbnRhaW5lcnMgPSBjb250YWluZXJzLmNvbmNhdChBcnJheS5mcm9tKHRoaXMuZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChub2RlKSkpO1xuICAgICAgICB9IGVsc2UgaWYgKEFycmF5LmlzQXJyYXkobm9kZSkpIHtcbiAgICAgICAgICBjb250YWluZXJzID0gY29udGFpbmVycy5jb25jYXQoQXJyYXkuZnJvbShub2RlKSk7XG4gICAgICAgIH0gZWxzZSBpZiAobm9kZSBpbnN0YW5jZW9mIHRoaXMud2luZG93Lk5vZGVMaXN0IHx8IG5vZGUgaW5zdGFuY2VvZiB0aGlzLndpbmRvdy5IVE1MQ29sbGVjdGlvbikge1xuICAgICAgICAgIGNvbnRhaW5lcnMgPSBjb250YWluZXJzLmNvbmNhdChBcnJheS5mcm9tKG5vZGUpKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBjb250YWluZXJzLnB1c2gobm9kZSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzFfMSkge1xuICAgICAgZV8xID0ge1xuICAgICAgICBlcnJvcjogZV8xXzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChub2Rlc18xXzEgJiYgIW5vZGVzXzFfMS5kb25lICYmIChfYSA9IG5vZGVzXzEucmV0dXJuKSkgX2EuY2FsbChub2Rlc18xKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzEpIHRocm93IGVfMS5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGNvbnRhaW5lcnM7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5jb250YWlucyA9IGZ1bmN0aW9uIChjb250YWluZXIsIG5vZGUpIHtcbiAgICByZXR1cm4gY29udGFpbmVyLmNvbnRhaW5zKG5vZGUpO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUucGFyZW50ID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gbm9kZS5wYXJlbnROb2RlO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuYXBwZW5kID0gZnVuY3Rpb24gKG5vZGUsIGNoaWxkKSB7XG4gICAgcmV0dXJuIG5vZGUuYXBwZW5kQ2hpbGQoY2hpbGQpO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuaW5zZXJ0ID0gZnVuY3Rpb24gKG5jaGlsZCwgb2NoaWxkKSB7XG4gICAgcmV0dXJuIHRoaXMucGFyZW50KG9jaGlsZCkuaW5zZXJ0QmVmb3JlKG5jaGlsZCwgb2NoaWxkKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnJlbW92ZSA9IGZ1bmN0aW9uIChjaGlsZCkge1xuICAgIHJldHVybiB0aGlzLnBhcmVudChjaGlsZCkucmVtb3ZlQ2hpbGQoY2hpbGQpO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUucmVwbGFjZSA9IGZ1bmN0aW9uIChubm9kZSwgb25vZGUpIHtcbiAgICByZXR1cm4gdGhpcy5wYXJlbnQob25vZGUpLnJlcGxhY2VDaGlsZChubm9kZSwgb25vZGUpO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuY2xvbmUgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHJldHVybiBub2RlLmNsb25lTm9kZSh0cnVlKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnNwbGl0ID0gZnVuY3Rpb24gKG5vZGUsIG4pIHtcbiAgICByZXR1cm4gbm9kZS5zcGxpdFRleHQobik7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5uZXh0ID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gbm9kZS5uZXh0U2libGluZztcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnByZXZpb3VzID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gbm9kZS5wcmV2aW91c1NpYmxpbmc7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5maXJzdENoaWxkID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gbm9kZS5maXJzdENoaWxkO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUubGFzdENoaWxkID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gbm9kZS5sYXN0Q2hpbGQ7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5jaGlsZE5vZGVzID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gQXJyYXkuZnJvbShub2RlLmNoaWxkTm9kZXMpO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuY2hpbGROb2RlID0gZnVuY3Rpb24gKG5vZGUsIGkpIHtcbiAgICByZXR1cm4gbm9kZS5jaGlsZE5vZGVzW2ldO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUua2luZCA9IGZ1bmN0aW9uIChub2RlKSB7XG4gICAgdmFyIG4gPSBub2RlLm5vZGVUeXBlO1xuICAgIHJldHVybiBuID09PSAxIHx8IG4gPT09IDMgfHwgbiA9PT0gOCA/IG5vZGUubm9kZU5hbWUudG9Mb3dlckNhc2UoKSA6ICcnO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUudmFsdWUgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHJldHVybiBub2RlLm5vZGVWYWx1ZSB8fCAnJztcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnRleHRDb250ZW50ID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gbm9kZS50ZXh0Q29udGVudDtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmlubmVySFRNTCA9IGZ1bmN0aW9uIChub2RlKSB7XG4gICAgcmV0dXJuIG5vZGUuaW5uZXJIVE1MO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUub3V0ZXJIVE1MID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICByZXR1cm4gbm9kZS5vdXRlckhUTUw7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5zZXJpYWxpemVYTUwgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHZhciBzZXJpYWxpemVyID0gbmV3IHRoaXMud2luZG93LlhNTFNlcmlhbGl6ZXIoKTtcbiAgICByZXR1cm4gc2VyaWFsaXplci5zZXJpYWxpemVUb1N0cmluZyhub2RlKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLnNldEF0dHJpYnV0ZSA9IGZ1bmN0aW9uIChub2RlLCBuYW1lLCB2YWx1ZSwgbnMpIHtcbiAgICBpZiAobnMgPT09IHZvaWQgMCkge1xuICAgICAgbnMgPSBudWxsO1xuICAgIH1cbiAgICBpZiAoIW5zKSB7XG4gICAgICByZXR1cm4gbm9kZS5zZXRBdHRyaWJ1dGUobmFtZSwgdmFsdWUpO1xuICAgIH1cbiAgICBuYW1lID0gbnMucmVwbGFjZSgvLipcXC8vLCAnJykgKyAnOicgKyBuYW1lLnJlcGxhY2UoL14uKjovLCAnJyk7XG4gICAgcmV0dXJuIG5vZGUuc2V0QXR0cmlidXRlTlMobnMsIG5hbWUsIHZhbHVlKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmdldEF0dHJpYnV0ZSA9IGZ1bmN0aW9uIChub2RlLCBuYW1lKSB7XG4gICAgcmV0dXJuIG5vZGUuZ2V0QXR0cmlidXRlKG5hbWUpO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUucmVtb3ZlQXR0cmlidXRlID0gZnVuY3Rpb24gKG5vZGUsIG5hbWUpIHtcbiAgICByZXR1cm4gbm9kZS5yZW1vdmVBdHRyaWJ1dGUobmFtZSk7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5oYXNBdHRyaWJ1dGUgPSBmdW5jdGlvbiAobm9kZSwgbmFtZSkge1xuICAgIHJldHVybiBub2RlLmhhc0F0dHJpYnV0ZShuYW1lKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmFsbEF0dHJpYnV0ZXMgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHJldHVybiBBcnJheS5mcm9tKG5vZGUuYXR0cmlidXRlcykubWFwKGZ1bmN0aW9uICh4KSB7XG4gICAgICByZXR1cm4ge1xuICAgICAgICBuYW1lOiB4Lm5hbWUsXG4gICAgICAgIHZhbHVlOiB4LnZhbHVlXG4gICAgICB9O1xuICAgIH0pO1xuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuYWRkQ2xhc3MgPSBmdW5jdGlvbiAobm9kZSwgbmFtZSkge1xuICAgIGlmIChub2RlLmNsYXNzTGlzdCkge1xuICAgICAgbm9kZS5jbGFzc0xpc3QuYWRkKG5hbWUpO1xuICAgIH0gZWxzZSB7XG4gICAgICBub2RlLmNsYXNzTmFtZSA9IChub2RlLmNsYXNzTmFtZSArICcgJyArIG5hbWUpLnRyaW0oKTtcbiAgICB9XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5yZW1vdmVDbGFzcyA9IGZ1bmN0aW9uIChub2RlLCBuYW1lKSB7XG4gICAgaWYgKG5vZGUuY2xhc3NMaXN0KSB7XG4gICAgICBub2RlLmNsYXNzTGlzdC5yZW1vdmUobmFtZSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIG5vZGUuY2xhc3NOYW1lID0gbm9kZS5jbGFzc05hbWUuc3BsaXQoLyAvKS5maWx0ZXIoZnVuY3Rpb24gKGMpIHtcbiAgICAgICAgcmV0dXJuIGMgIT09IG5hbWU7XG4gICAgICB9KS5qb2luKCcgJyk7XG4gICAgfVxuICB9O1xuICBIVE1MQWRhcHRvci5wcm90b3R5cGUuaGFzQ2xhc3MgPSBmdW5jdGlvbiAobm9kZSwgbmFtZSkge1xuICAgIGlmIChub2RlLmNsYXNzTGlzdCkge1xuICAgICAgcmV0dXJuIG5vZGUuY2xhc3NMaXN0LmNvbnRhaW5zKG5hbWUpO1xuICAgIH1cbiAgICByZXR1cm4gbm9kZS5jbGFzc05hbWUuc3BsaXQoLyAvKS5pbmRleE9mKG5hbWUpID49IDA7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5zZXRTdHlsZSA9IGZ1bmN0aW9uIChub2RlLCBuYW1lLCB2YWx1ZSkge1xuICAgIG5vZGUuc3R5bGVbbmFtZV0gPSB2YWx1ZTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmdldFN0eWxlID0gZnVuY3Rpb24gKG5vZGUsIG5hbWUpIHtcbiAgICByZXR1cm4gbm9kZS5zdHlsZVtuYW1lXTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmFsbFN0eWxlcyA9IGZ1bmN0aW9uIChub2RlKSB7XG4gICAgcmV0dXJuIG5vZGUuc3R5bGUuY3NzVGV4dDtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmluc2VydFJ1bGVzID0gZnVuY3Rpb24gKG5vZGUsIHJ1bGVzKSB7XG4gICAgdmFyIGVfMiwgX2E7XG4gICAgdHJ5IHtcbiAgICAgIGZvciAodmFyIF9iID0gX192YWx1ZXMocnVsZXMucmV2ZXJzZSgpKSwgX2MgPSBfYi5uZXh0KCk7ICFfYy5kb25lOyBfYyA9IF9iLm5leHQoKSkge1xuICAgICAgICB2YXIgcnVsZSA9IF9jLnZhbHVlO1xuICAgICAgICB0cnkge1xuICAgICAgICAgIG5vZGUuc2hlZXQuaW5zZXJ0UnVsZShydWxlLCAwKTtcbiAgICAgICAgfSBjYXRjaCAoZSkge1xuICAgICAgICAgIGNvbnNvbGUud2FybihcIk1hdGhKYXg6IGNhbid0IGluc2VydCBjc3MgcnVsZSAnXCIuY29uY2F0KHJ1bGUsIFwiJzogXCIpLmNvbmNhdChlLm1lc3NhZ2UpKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0gY2F0Y2ggKGVfMl8xKSB7XG4gICAgICBlXzIgPSB7XG4gICAgICAgIGVycm9yOiBlXzJfMVxuICAgICAgfTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgaWYgKF9jICYmICFfYy5kb25lICYmIChfYSA9IF9iLnJldHVybikpIF9hLmNhbGwoX2IpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgaWYgKGVfMikgdGhyb3cgZV8yLmVycm9yO1xuICAgICAgfVxuICAgIH1cbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmZvbnRTaXplID0gZnVuY3Rpb24gKG5vZGUpIHtcbiAgICB2YXIgc3R5bGUgPSB0aGlzLndpbmRvdy5nZXRDb21wdXRlZFN0eWxlKG5vZGUpO1xuICAgIHJldHVybiBwYXJzZUZsb2F0KHN0eWxlLmZvbnRTaXplKTtcbiAgfTtcbiAgSFRNTEFkYXB0b3IucHJvdG90eXBlLmZvbnRGYW1pbHkgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHZhciBzdHlsZSA9IHRoaXMud2luZG93LmdldENvbXB1dGVkU3R5bGUobm9kZSk7XG4gICAgcmV0dXJuIHN0eWxlLmZvbnRGYW1pbHkgfHwgJyc7XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5ub2RlU2l6ZSA9IGZ1bmN0aW9uIChub2RlLCBlbSwgbG9jYWwpIHtcbiAgICBpZiAoZW0gPT09IHZvaWQgMCkge1xuICAgICAgZW0gPSAxO1xuICAgIH1cbiAgICBpZiAobG9jYWwgPT09IHZvaWQgMCkge1xuICAgICAgbG9jYWwgPSBmYWxzZTtcbiAgICB9XG4gICAgaWYgKGxvY2FsICYmIG5vZGUuZ2V0QkJveCkge1xuICAgICAgdmFyIF9hID0gbm9kZS5nZXRCQm94KCksXG4gICAgICAgIHdpZHRoID0gX2Eud2lkdGgsXG4gICAgICAgIGhlaWdodCA9IF9hLmhlaWdodDtcbiAgICAgIHJldHVybiBbd2lkdGggLyBlbSwgaGVpZ2h0IC8gZW1dO1xuICAgIH1cbiAgICByZXR1cm4gW25vZGUub2Zmc2V0V2lkdGggLyBlbSwgbm9kZS5vZmZzZXRIZWlnaHQgLyBlbV07XG4gIH07XG4gIEhUTUxBZGFwdG9yLnByb3RvdHlwZS5ub2RlQkJveCA9IGZ1bmN0aW9uIChub2RlKSB7XG4gICAgdmFyIF9hID0gbm9kZS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKSxcbiAgICAgIGxlZnQgPSBfYS5sZWZ0LFxuICAgICAgcmlnaHQgPSBfYS5yaWdodCxcbiAgICAgIHRvcCA9IF9hLnRvcCxcbiAgICAgIGJvdHRvbSA9IF9hLmJvdHRvbTtcbiAgICByZXR1cm4ge1xuICAgICAgbGVmdDogbGVmdCxcbiAgICAgIHJpZ2h0OiByaWdodCxcbiAgICAgIHRvcDogdG9wLFxuICAgICAgYm90dG9tOiBib3R0b21cbiAgICB9O1xuICB9O1xuICByZXR1cm4gSFRNTEFkYXB0b3I7XG59KERPTUFkYXB0b3JfanNfMS5BYnN0cmFjdERPTUFkYXB0b3IpO1xuZXhwb3J0cy5IVE1MQWRhcHRvciA9IEhUTUxBZGFwdG9yOyIsIlwidXNlIHN0cmljdFwiO1xuXG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5icm93c2VyQWRhcHRvciA9IHZvaWQgMDtcbnZhciBIVE1MQWRhcHRvcl9qc18xID0gcmVxdWlyZShcIi4vSFRNTEFkYXB0b3IuanNcIik7XG5mdW5jdGlvbiBicm93c2VyQWRhcHRvcigpIHtcbiAgcmV0dXJuIG5ldyBIVE1MQWRhcHRvcl9qc18xLkhUTUxBZGFwdG9yKHdpbmRvdyk7XG59XG5leHBvcnRzLmJyb3dzZXJBZGFwdG9yID0gYnJvd3NlckFkYXB0b3I7IiwiXCJ1c2Ugc3RyaWN0XCI7XG5cbnZhciBfX3ZhbHVlcyA9IHRoaXMgJiYgdGhpcy5fX3ZhbHVlcyB8fCBmdW5jdGlvbiAobykge1xuICB2YXIgcyA9IHR5cGVvZiBTeW1ib2wgPT09IFwiZnVuY3Rpb25cIiAmJiBTeW1ib2wuaXRlcmF0b3IsXG4gICAgbSA9IHMgJiYgb1tzXSxcbiAgICBpID0gMDtcbiAgaWYgKG0pIHJldHVybiBtLmNhbGwobyk7XG4gIGlmIChvICYmIHR5cGVvZiBvLmxlbmd0aCA9PT0gXCJudW1iZXJcIikgcmV0dXJuIHtcbiAgICBuZXh0OiBmdW5jdGlvbiAoKSB7XG4gICAgICBpZiAobyAmJiBpID49IG8ubGVuZ3RoKSBvID0gdm9pZCAwO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdmFsdWU6IG8gJiYgb1tpKytdLFxuICAgICAgICBkb25lOiAhb1xuICAgICAgfTtcbiAgICB9XG4gIH07XG4gIHRocm93IG5ldyBUeXBlRXJyb3IocyA/IFwiT2JqZWN0IGlzIG5vdCBpdGVyYWJsZS5cIiA6IFwiU3ltYm9sLml0ZXJhdG9yIGlzIG5vdCBkZWZpbmVkLlwiKTtcbn07XG5PYmplY3QuZGVmaW5lUHJvcGVydHkoZXhwb3J0cywgXCJfX2VzTW9kdWxlXCIsIHtcbiAgdmFsdWU6IHRydWVcbn0pO1xuZXhwb3J0cy5BYnN0cmFjdERPTUFkYXB0b3IgPSB2b2lkIDA7XG52YXIgQWJzdHJhY3RET01BZGFwdG9yID0gZnVuY3Rpb24gKCkge1xuICBmdW5jdGlvbiBBYnN0cmFjdERPTUFkYXB0b3IoZG9jdW1lbnQpIHtcbiAgICBpZiAoZG9jdW1lbnQgPT09IHZvaWQgMCkge1xuICAgICAgZG9jdW1lbnQgPSBudWxsO1xuICAgIH1cbiAgICB0aGlzLmRvY3VtZW50ID0gZG9jdW1lbnQ7XG4gIH1cbiAgQWJzdHJhY3RET01BZGFwdG9yLnByb3RvdHlwZS5ub2RlID0gZnVuY3Rpb24gKGtpbmQsIGRlZiwgY2hpbGRyZW4sIG5zKSB7XG4gICAgdmFyIGVfMSwgX2E7XG4gICAgaWYgKGRlZiA9PT0gdm9pZCAwKSB7XG4gICAgICBkZWYgPSB7fTtcbiAgICB9XG4gICAgaWYgKGNoaWxkcmVuID09PSB2b2lkIDApIHtcbiAgICAgIGNoaWxkcmVuID0gW107XG4gICAgfVxuICAgIHZhciBub2RlID0gdGhpcy5jcmVhdGUoa2luZCwgbnMpO1xuICAgIHRoaXMuc2V0QXR0cmlidXRlcyhub2RlLCBkZWYpO1xuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBjaGlsZHJlbl8xID0gX192YWx1ZXMoY2hpbGRyZW4pLCBjaGlsZHJlbl8xXzEgPSBjaGlsZHJlbl8xLm5leHQoKTsgIWNoaWxkcmVuXzFfMS5kb25lOyBjaGlsZHJlbl8xXzEgPSBjaGlsZHJlbl8xLm5leHQoKSkge1xuICAgICAgICB2YXIgY2hpbGQgPSBjaGlsZHJlbl8xXzEudmFsdWU7XG4gICAgICAgIHRoaXMuYXBwZW5kKG5vZGUsIGNoaWxkKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzFfMSkge1xuICAgICAgZV8xID0ge1xuICAgICAgICBlcnJvcjogZV8xXzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChjaGlsZHJlbl8xXzEgJiYgIWNoaWxkcmVuXzFfMS5kb25lICYmIChfYSA9IGNoaWxkcmVuXzEucmV0dXJuKSkgX2EuY2FsbChjaGlsZHJlbl8xKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzEpIHRocm93IGVfMS5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIG5vZGU7XG4gIH07XG4gIEFic3RyYWN0RE9NQWRhcHRvci5wcm90b3R5cGUuc2V0QXR0cmlidXRlcyA9IGZ1bmN0aW9uIChub2RlLCBkZWYpIHtcbiAgICB2YXIgZV8yLCBfYSwgZV8zLCBfYiwgZV80LCBfYztcbiAgICBpZiAoZGVmLnN0eWxlICYmIHR5cGVvZiBkZWYuc3R5bGUgIT09ICdzdHJpbmcnKSB7XG4gICAgICB0cnkge1xuICAgICAgICBmb3IgKHZhciBfZCA9IF9fdmFsdWVzKE9iamVjdC5rZXlzKGRlZi5zdHlsZSkpLCBfZSA9IF9kLm5leHQoKTsgIV9lLmRvbmU7IF9lID0gX2QubmV4dCgpKSB7XG4gICAgICAgICAgdmFyIGtleSA9IF9lLnZhbHVlO1xuICAgICAgICAgIHRoaXMuc2V0U3R5bGUobm9kZSwga2V5LnJlcGxhY2UoLy0oW2Etel0pL2csIGZ1bmN0aW9uIChfbSwgYykge1xuICAgICAgICAgICAgcmV0dXJuIGMudG9VcHBlckNhc2UoKTtcbiAgICAgICAgICB9KSwgZGVmLnN0eWxlW2tleV0pO1xuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlXzJfMSkge1xuICAgICAgICBlXzIgPSB7XG4gICAgICAgICAgZXJyb3I6IGVfMl8xXG4gICAgICAgIH07XG4gICAgICB9IGZpbmFsbHkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGlmIChfZSAmJiAhX2UuZG9uZSAmJiAoX2EgPSBfZC5yZXR1cm4pKSBfYS5jYWxsKF9kKTtcbiAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICBpZiAoZV8yKSB0aHJvdyBlXzIuZXJyb3I7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKGRlZi5wcm9wZXJ0aWVzKSB7XG4gICAgICB0cnkge1xuICAgICAgICBmb3IgKHZhciBfZiA9IF9fdmFsdWVzKE9iamVjdC5rZXlzKGRlZi5wcm9wZXJ0aWVzKSksIF9nID0gX2YubmV4dCgpOyAhX2cuZG9uZTsgX2cgPSBfZi5uZXh0KCkpIHtcbiAgICAgICAgICB2YXIga2V5ID0gX2cudmFsdWU7XG4gICAgICAgICAgbm9kZVtrZXldID0gZGVmLnByb3BlcnRpZXNba2V5XTtcbiAgICAgICAgfVxuICAgICAgfSBjYXRjaCAoZV8zXzEpIHtcbiAgICAgICAgZV8zID0ge1xuICAgICAgICAgIGVycm9yOiBlXzNfMVxuICAgICAgICB9O1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICBpZiAoX2cgJiYgIV9nLmRvbmUgJiYgKF9iID0gX2YucmV0dXJuKSkgX2IuY2FsbChfZik7XG4gICAgICAgIH0gZmluYWxseSB7XG4gICAgICAgICAgaWYgKGVfMykgdGhyb3cgZV8zLmVycm9yO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICAgIHRyeSB7XG4gICAgICBmb3IgKHZhciBfaCA9IF9fdmFsdWVzKE9iamVjdC5rZXlzKGRlZikpLCBfaiA9IF9oLm5leHQoKTsgIV9qLmRvbmU7IF9qID0gX2gubmV4dCgpKSB7XG4gICAgICAgIHZhciBrZXkgPSBfai52YWx1ZTtcbiAgICAgICAgaWYgKChrZXkgIT09ICdzdHlsZScgfHwgdHlwZW9mIGRlZi5zdHlsZSA9PT0gJ3N0cmluZycpICYmIGtleSAhPT0gJ3Byb3BlcnRpZXMnKSB7XG4gICAgICAgICAgdGhpcy5zZXRBdHRyaWJ1dGUobm9kZSwga2V5LCBkZWZba2V5XSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9IGNhdGNoIChlXzRfMSkge1xuICAgICAgZV80ID0ge1xuICAgICAgICBlcnJvcjogZV80XzFcbiAgICAgIH07XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGlmIChfaiAmJiAhX2ouZG9uZSAmJiAoX2MgPSBfaC5yZXR1cm4pKSBfYy5jYWxsKF9oKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGlmIChlXzQpIHRocm93IGVfNC5lcnJvcjtcbiAgICAgIH1cbiAgICB9XG4gIH07XG4gIEFic3RyYWN0RE9NQWRhcHRvci5wcm90b3R5cGUucmVwbGFjZSA9IGZ1bmN0aW9uIChubm9kZSwgb25vZGUpIHtcbiAgICB0aGlzLmluc2VydChubm9kZSwgb25vZGUpO1xuICAgIHRoaXMucmVtb3ZlKG9ub2RlKTtcbiAgICByZXR1cm4gb25vZGU7XG4gIH07XG4gIEFic3RyYWN0RE9NQWRhcHRvci5wcm90b3R5cGUuY2hpbGROb2RlID0gZnVuY3Rpb24gKG5vZGUsIGkpIHtcbiAgICByZXR1cm4gdGhpcy5jaGlsZE5vZGVzKG5vZGUpW2ldO1xuICB9O1xuICBBYnN0cmFjdERPTUFkYXB0b3IucHJvdG90eXBlLmFsbENsYXNzZXMgPSBmdW5jdGlvbiAobm9kZSkge1xuICAgIHZhciBjbGFzc2VzID0gdGhpcy5nZXRBdHRyaWJ1dGUobm9kZSwgJ2NsYXNzJyk7XG4gICAgcmV0dXJuICFjbGFzc2VzID8gW10gOiBjbGFzc2VzLnJlcGxhY2UoLyAgKy9nLCAnICcpLnJlcGxhY2UoL14gLywgJycpLnJlcGxhY2UoLyAkLywgJycpLnNwbGl0KC8gLyk7XG4gIH07XG4gIHJldHVybiBBYnN0cmFjdERPTUFkYXB0b3I7XG59KCk7XG5leHBvcnRzLkFic3RyYWN0RE9NQWRhcHRvciA9IEFic3RyYWN0RE9NQWRhcHRvcjsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=