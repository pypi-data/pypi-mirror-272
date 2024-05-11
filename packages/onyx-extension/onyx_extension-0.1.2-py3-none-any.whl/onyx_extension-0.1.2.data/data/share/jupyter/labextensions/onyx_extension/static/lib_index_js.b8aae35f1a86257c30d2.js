"use strict";
(self["webpackChunkonyx_extension"] = self["webpackChunkonyx_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/App.js":
/*!********************!*\
  !*** ./lib/App.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ReactAppWidget: () => (/* binding */ ReactAppWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _enums__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./enums */ "./lib/enums.js");


//import App from '../../react-prototype/src/App'

function MyComponent() {
    return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null, "Onyx Extension");
}
class ReactAppWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor() {
        super();
        this.addClass(_enums__WEBPACK_IMPORTED_MODULE_2__.EXTENSION_CSS_CLASSNAME);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(MyComponent, null));
    }
}


/***/ }),

/***/ "./lib/activate.js":
/*!*************************!*\
  !*** ./lib/activate.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   activate: () => (/* binding */ activate)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _enums__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./enums */ "./lib/enums.js");
/* harmony import */ var _App__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./App */ "./lib/App.js");



const activate = (app, palette, restorer, launcher) => {
    console.log(`JupyterLab extension ${_enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_ID} is activated!`);
    // Create a single widget
    let widget;
    // Add an application command
    const command = _enums__WEBPACK_IMPORTED_MODULE_1__.OPEN_COMMAND;
    app.commands.addCommand(command, {
        label: _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_NAME,
        execute: () => {
            if (!widget) {
                const content = new _App__WEBPACK_IMPORTED_MODULE_2__.ReactAppWidget();
                widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                widget.id = _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_ID;
                widget.title.label = _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_NAME;
                widget.title.closable = true;
            }
            if (!tracker.has(widget)) {
                tracker.add(widget);
            }
            if (!widget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(widget, 'main');
            }
            // Activate the widget
            app.shell.activateById(widget.id);
        },
    });
    // Add the command to the palette.
    palette.addItem({ command, category: _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_NAME });
    const launcher_item = {
        command: command,
        args: {
            newBrowserTab: true,
            title: _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_NAME,
            id: _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_ID
        },
        category: 'Other',
        rank: 10
    };
    launcher_item.kernelIconUrl = '../style/icons/server.svg';
    launcher.add(launcher_item);
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({
        namespace: _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_ID,
    });
    restorer.restore(tracker, {
        command: _enums__WEBPACK_IMPORTED_MODULE_1__.OPEN_COMMAND,
        name: () => _enums__WEBPACK_IMPORTED_MODULE_1__.EXTENSION_ID,
    });
};


/***/ }),

/***/ "./lib/enums.js":
/*!**********************!*\
  !*** ./lib/enums.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   EXTENSION_CSS_CLASSNAME: () => (/* binding */ EXTENSION_CSS_CLASSNAME),
/* harmony export */   EXTENSION_ID: () => (/* binding */ EXTENSION_ID),
/* harmony export */   EXTENSION_NAME: () => (/* binding */ EXTENSION_NAME),
/* harmony export */   OPEN_COMMAND: () => (/* binding */ OPEN_COMMAND)
/* harmony export */ });
const EXTENSION_ID = 'onyx_extension';
const EXTENSION_NAME = 'Climb-Onyx-UI';
const OPEN_COMMAND = 'jle:open';
const EXTENSION_CSS_CLASSNAME = 'jl-ReactAppWidget';


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _activate__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./activate */ "./lib/activate.js");




const extension = {
    id: 'jl-extension-env',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher],
    activate: _activate__WEBPACK_IMPORTED_MODULE_3__.activate,
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b8aae35f1a86257c30d2.js.map