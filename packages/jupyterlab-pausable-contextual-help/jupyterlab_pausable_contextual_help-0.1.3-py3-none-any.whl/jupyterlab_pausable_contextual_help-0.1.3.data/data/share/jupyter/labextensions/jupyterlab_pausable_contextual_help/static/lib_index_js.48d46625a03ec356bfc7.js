"use strict";
(self["webpackChunkjupyterlab_pausable_contextual_help"] = self["webpackChunkjupyterlab_pausable_contextual_help"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InspectionHandler: () => (/* binding */ InspectionHandler)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * An object that handles code inspection.
 */
class InspectionHandler {
    /**
     * Construct a new inspection handler for a widget.
     */
    constructor(options) {
        this._cleared = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._editor = null;
        this._inspected = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._isDisposed = false;
        this._pending = 0;
        this._standby = true;
        this._lastInspectedReply = null;
        this._connector = options.connector;
        this._rendermime = options.rendermime;
        this._debouncer = new _lumino_polling__WEBPACK_IMPORTED_MODULE_3__.Debouncer(this.onEditorChange.bind(this), 250);
    }
    /**
     * A signal emitted when the myinspector should clear all items.
     */
    get cleared() {
        return this._cleared;
    }
    /**
     * A signal emitted when the handler is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * A signal emitted when an myinspector value is generated.
     */
    get inspected() {
        return this._inspected;
    }
    /**
     * The editor widget used by the inspection handler.
     */
    get editor() {
        return this._editor;
    }
    set editor(newValue) {
        if (newValue === this._editor) {
            return;
        }
        // Remove all of our listeners.
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.disconnectReceiver(this);
        const editor = (this._editor = newValue);
        if (editor) {
            // Clear the myinspector in preparation for a new editor.
            this._cleared.emit(void 0);
            // Call onEditorChange to cover the case where the user changes
            // the active cell
            this.onEditorChange();
            editor.model.selections.changed.connect(this._onChange, this);
            editor.model.sharedModel.changed.connect(this._onChange, this);
        }
    }
    /**
     * Indicates whether the handler makes API inspection requests or stands by.
     *
     * #### Notes
     * The use case for this attribute is to limit the API traffic when no
     * myinspector is visible.
     */
    get standby() {
        return this._standby;
    }
    set standby(value) {
        this._standby = value;
    }
    /**
     * Get whether the inspection handler is disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._debouncer.dispose();
        this._disposed.emit(void 0);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.clearData(this);
    }
    /**
     * Handle a text changed signal from an editor.
     *
     * #### Notes
     * Update the hints myinspector based on a text change.
     */
    onEditorChange(customText) {
        // If the handler is in standby mode, bail.
        if (this._standby) {
            return;
        }
        const editor = this.editor;
        if (!editor) {
            return;
        }
        const text = customText ? customText : editor.model.sharedModel.getSource();
        const position = editor.getCursorPosition();
        const offset = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.Text.jsIndexToCharIndex(editor.getOffsetAt(position), text);
        const update = { content: null };
        const pending = ++this._pending;
        void this._connector
            .fetch({ offset, text })
            .then(reply => {
            // If handler has been disposed or a newer request is pending, bail.
            if (!reply || this.isDisposed || pending !== this._pending) {
                this._lastInspectedReply = null;
                this._inspected.emit(update);
                return;
            }
            const { data } = reply;
            // Do not update if there would be no change.
            if (this._lastInspectedReply &&
                _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(this._lastInspectedReply, data)) {
                return;
            }
            const mimeType = this._rendermime.preferredMimeType(data);
            if (mimeType) {
                const widget = this._rendermime.createRenderer(mimeType);
                const model = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.MimeModel({ data });
                void widget.renderModel(model);
                update.content = widget;
            }
            this._lastInspectedReply = reply.data;
            this._inspected.emit(update);
        })
            .catch(reason => {
            // Since almost all failures are benign, fail silently.
            this._lastInspectedReply = null;
            this._inspected.emit(update);
        });
    }
    /**
     * Handle changes to the editor state, debouncing.
     */
    _onChange() {
        void this._debouncer.invoke();
    }
}


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
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _myinspector__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./myinspector */ "./lib/myinspector.js");
/* harmony import */ var _kernelconnector__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./kernelconnector */ "./lib/kernelconnector.js");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// export * from './handler';
// export * from './myinspector';
// export * from './kernelconnector';
// export * from './tokens';
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// import { ISettingRegistry } from '@jupyterlab/settingregistry';


//   import {
//     IMyInspector,
//     InspectionHandler,
//     MyInspectorPanel,
//     KernelConnector
//   } from '@jupyterlab/inspector';








/**
 * The command IDs used by the myinspector plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'myinspector:open';
    CommandIDs.close = 'myinspector:close';
    CommandIDs.toggle = 'myinspector:toggle';
    CommandIDs.trigger = 'myinspector:trigger';
    CommandIDs.toggleStandby = 'myinspector:toggleStandby';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing code introspection.
 */
const myinspector = {
    id: 'jupyterlab_pausable_contextual_help:myinspector',
    description: 'Provides the pausable code introspection widget.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _tokens__WEBPACK_IMPORTED_MODULE_7__.IMyInspector,
    autoStart: true,
    activate: (app, translator, palette, launcher, restorer) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const caption = trans.__('Manually updating code documentation from the active kernel');
        const openedLabel = trans.__('My Contextual Help');
        const namespace = 'myinspector';
        const datasetKey = 'jpMyInspector';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace
        });
        function isMyInspectorOpen() {
            return myinspector && !myinspector.isDisposed;
        }
        function isStandby() {
            // return myinspector && myinspector.content && myinspector.content.source && myinspector.content.source.standby;
            if (myinspector && myinspector.content && myinspector.content.source) {
                return myinspector.content.source.standby;
            }
            return false;
        }
        let source = null;
        let myinspector;
        function openMyInspector(args) {
            var _a;
            if (!isMyInspectorOpen()) {
                myinspector = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                    content: new _myinspector__WEBPACK_IMPORTED_MODULE_8__.MyInspectorPanel({ translator })
                });
                myinspector.id = 'jp-myinspector';
                myinspector.title.label = openedLabel;
                myinspector.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.inspectorIcon;
                void tracker.add(myinspector);
                source = source && !source.isDisposed ? source : null;
                myinspector.content.source = source;
                (_a = myinspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(args);
            }
            if (!myinspector.isAttached) {
                shell.add(myinspector, 'main', {
                    activate: false,
                    mode: 'split-right',
                    type: 'MyInspector'
                });
            }
            shell.activateById(myinspector.id);
            document.body.dataset[datasetKey] = 'open';
            return myinspector;
        }
        function closeMyInspector() {
            myinspector.dispose();
            delete document.body.dataset[datasetKey];
        }
        // Add myinspector:open command to registry.
        const showLabel = trans.__('Open My Contextual Help');
        commands.addCommand(CommandIDs.open, {
            caption,
            isEnabled: () => !myinspector ||
                myinspector.isDisposed ||
                !myinspector.isAttached ||
                !myinspector.isVisible,
            label: showLabel,
            icon: args => (args.isLauncher ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.inspectorIcon : undefined),
            execute: args => {
                var _a;
                const text = args && args.text;
                const refresh = args && args.refresh;
                // if myinspector is open, see if we need a refresh
                if (isMyInspectorOpen() && refresh)
                    (_a = myinspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(text);
                else
                    openMyInspector(text);
            }
        });
        // Add myinspector:close command to registry.
        const closeLabel = trans.__('Hide My Contextual Help');
        commands.addCommand(CommandIDs.close, {
            caption,
            isEnabled: () => isMyInspectorOpen(),
            label: closeLabel,
            icon: args => (args.isLauncher ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.inspectorIcon : undefined),
            execute: () => closeMyInspector()
        });
        // Add myinspector:toggle command to registry.
        const toggleLabel = trans.__('Show My Contextual Help');
        commands.addCommand(CommandIDs.toggle, {
            caption,
            label: toggleLabel,
            isToggled: () => isMyInspectorOpen(),
            execute: args => {
                if (isMyInspectorOpen()) {
                    closeMyInspector();
                }
                else {
                    const text = args && args.text;
                    openMyInspector(text);
                }
            }
        });
        // Add myinspector:trigger command to registry.
        const triggerLabel = trans.__('Trigger My Contextual Help');
        commands.addCommand(CommandIDs.trigger, {
            caption,
            isEnabled: () => isStandby(),
            label: triggerLabel,
            execute: () => {
                var _a;
                if (myinspector && myinspector.content && myinspector.content.source && isStandby()) {
                    myinspector.content.source.standby = false;
                    (_a = myinspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange();
                    myinspector.content.source.standby = true;
                }
            }
        });
        // Add myinspector:toggleStandby command to registry.
        const toggleStandbyLabel = trans.__('Auto Update My Contextual Help');
        commands.addCommand(CommandIDs.toggleStandby, {
            caption,
            isToggled: () => !isStandby(),
            label: toggleStandbyLabel,
            execute: () => {
                if (myinspector && myinspector.content && myinspector.content.source) {
                    if (isStandby()) {
                        myinspector.content.source.standby = false;
                    }
                    else {
                        myinspector.content.source.standby = true;
                    }
                }
            }
        });
        // Add open command to launcher if possible.
        if (launcher) {
            launcher.add({ command: CommandIDs.open, args: { isLauncher: true } });
        }
        // Add toggle command to command palette if possible.
        if (palette) {
            palette.addItem({ command: CommandIDs.toggle, category: toggleLabel });
        }
        // Handle state restoration.
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.toggle,
                name: () => 'myinspector'
            });
        }
        // Create a proxy to pass the `source` to the current myinspector.
        const proxy = Object.defineProperty({}, 'source', {
            get: () => !myinspector || myinspector.isDisposed ? null : myinspector.content.source,
            set: (src) => {
                source = src && !src.isDisposed ? src : null;
                if (myinspector && !myinspector.isDisposed) {
                    myinspector.content.source = source;
                }
            }
        });
        return proxy;
    }
};
/**
 * An extension that registers consoles for inspection.
 */
const consoles = {
    // FIXME This should be in @jupyterlab/console-extension
    id: 'jupyterlab_pausable_contextual_help:consoles',
    description: 'Adds my code introspection support to consoles.',
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_7__.IMyInspector, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, consoles, labShell, translator) => {
        // Maintain association of new consoles with their respective handlers.
        const handlers = {};
        // Create a handler for each console that is created.
        consoles.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.console.sessionContext;
            const rendermime = parent.console.rendermime;
            const connector = new _kernelconnector__WEBPACK_IMPORTED_MODULE_9__.KernelConnector({ sessionContext });
            const handler = new _handler__WEBPACK_IMPORTED_MODULE_10__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.console.promptCell;
            handler.editor = cell && cell.editor;
            // Listen for prompt creation.
            parent.console.promptCellCreated.connect((sender, cell) => {
                handler.editor = cell && cell.editor;
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of console instances and set myinspector source.
        const setSource = (widget) => {
            if (widget && consoles.has(widget) && handlers[widget.id]) {
                manager.source = handlers[widget.id];
            }
        };
        labShell.currentChanged.connect((_, args) => setSource(args.newValue));
        void app.restored.then(() => setSource(labShell.currentWidget));
        app.contextMenu.addItem({
            command: CommandIDs.toggle,
            selector: '.jp-CodeConsole-promptCell'
        });
        app.contextMenu.addItem({
            command: CommandIDs.toggleStandby,
            selector: '.jp-CodeConsole-promptCell'
        });
    }
};
/**
 * An extension that registers notebooks for inspection.
 */
const notebooks = {
    // FIXME This should be in @jupyterlab/notebook-extension
    id: 'jupyterlab_pausable_contextual_help:notebooks',
    description: 'Adds code introspection to notebooks.',
    requires: [_tokens__WEBPACK_IMPORTED_MODULE_7__.IMyInspector, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.INotebookTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, notebooks, labShell) => {
        // Maintain association of new notebooks with their respective handlers.
        const handlers = {};
        // Create a handler for each notebook that is created.
        notebooks.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.sessionContext;
            const rendermime = parent.content.rendermime;
            const connector = new _kernelconnector__WEBPACK_IMPORTED_MODULE_9__.KernelConnector({ sessionContext });
            const handler = new _handler__WEBPACK_IMPORTED_MODULE_10__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.content.activeCell;
            handler.editor = cell && cell.editor;
            // Listen for active cell changes.
            parent.content.activeCellChanged.connect((sender, cell) => {
                void (cell === null || cell === void 0 ? void 0 : cell.ready.then(() => {
                    if (cell === parent.content.activeCell) {
                        handler.editor = cell.editor;
                    }
                }));
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of notebook instances and set myinspector source.
        const setSource = (widget) => {
            if (widget && notebooks.has(widget) && handlers[widget.id]) {
                manager.source = handlers[widget.id];
            }
        };
        labShell.currentChanged.connect((_, args) => setSource(args.newValue));
        void app.restored.then(() => setSource(labShell.currentWidget));
        app.contextMenu.addItem({
            command: CommandIDs.toggle,
            selector: '.jp-Notebook'
        });
        app.contextMenu.addItem({
            command: CommandIDs.toggleStandby,
            selector: '.jp-Notebook'
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [myinspector, consoles, notebooks];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/kernelconnector.js":
/*!********************************!*\
  !*** ./lib/kernelconnector.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   KernelConnector: () => (/* binding */ KernelConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The default connector for making inspection requests from the Jupyter API.
 */
class KernelConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new kernel connector for inspection requests.
     *
     * @param options - The instantiation options for the kernel connector.
     */
    constructor(options) {
        super();
        this._sessionContext = options.sessionContext;
    }
    /**
     * Fetch inspection requests.
     *
     * @param request - The inspection request text and details.
     */
    fetch(request) {
        var _a;
        const kernel = (_a = this._sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return Promise.reject(new Error('Inspection fetch requires a kernel.'));
        }
        const contents = {
            code: request.text,
            cursor_pos: request.offset,
            detail_level: 1
        };
        return kernel.requestInspect(contents).then(msg => {
            const response = msg.content;
            if (response.status !== 'ok' || !response.found) {
                throw new Error('Inspection fetch failed to return successfully.');
            }
            return { data: response.data, metadata: response.metadata };
        });
    }
}


/***/ }),

/***/ "./lib/myinspector.js":
/*!****************************!*\
  !*** ./lib/myinspector.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   MyInspectorPanel: () => (/* binding */ MyInspectorPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to myinspector panels.
 */
const PANEL_CLASS = 'jp-MyInspector';
/**
 * The class name added to myinspector content.
 */
const CONTENT_CLASS = 'jp-MyInspector-content';
/**
 * The class name added to default myinspector content.
 */
const DEFAULT_CONTENT_CLASS = 'jp-MyInspector-default-content';
/**
 * A panel which contains a set of myinspectors.
 */
class MyInspectorPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel {
    /**
     * Construct an myinspector.
     */
    constructor(options = {}) {
        super();
        this._source = null;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        if (options.initialContent instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget) {
            this._content = options.initialContent;
        }
        else if (typeof options.initialContent === 'string') {
            this._content = MyInspectorPanel._generateContentWidget(`<p>${options.initialContent}</p>`);
        }
        else {
            this._content = MyInspectorPanel._generateContentWidget('<p>' +
                this._trans.__('Press F1 on a function to see documentation.') +
                '</p>');
        }
        this.addClass(PANEL_CLASS);
        this.layout.addWidget(this._content);
    }
    /**
     * Print in iframe
     */
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.printWidget(this);
    }
    /**
     * The source of events the myinspector panel listens for.
     */
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            return;
        }
        // Disconnect old signal handler.
        if (this._source) {
            this._source.standby = true;
            this._source.inspected.disconnect(this.onMyInspectorUpdate, this);
            this._source.disposed.disconnect(this.onSourceDisposed, this);
        }
        // Reject a source that is already disposed.
        if (source && source.isDisposed) {
            source = null;
        }
        // Update source.
        this._source = source;
        // Connect new signal handler.
        if (this._source) {
            //   this._source.standby = false;
            this._source.inspected.connect(this.onMyInspectorUpdate, this);
            this._source.disposed.connect(this.onSourceDisposed, this);
        }
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.source = null;
        super.dispose();
    }
    /**
     * Handle myinspector update signals.
     */
    onMyInspectorUpdate(sender, args) {
        const { content } = args;
        // Update the content of the myinspector widget.
        if (!content || content === this._content) {
            return;
        }
        this._content.dispose();
        this._content = content;
        content.addClass(CONTENT_CLASS);
        this.layout.addWidget(content);
    }
    /**
     * Handle source disposed signals.
     */
    onSourceDisposed(sender, args) {
        this.source = null;
    }
    /**
     * Generate content widget from string
     */
    static _generateContentWidget(message) {
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget();
        widget.node.innerHTML = message;
        widget.addClass(CONTENT_CLASS);
        widget.addClass(DEFAULT_CONTENT_CLASS);
        return widget;
    }
}


/***/ }),

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IMyInspector: () => (/* binding */ IMyInspector)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The myinspector panel token.
 */
const IMyInspector = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/inspector:IMyInspector', `A service for adding contextual help to widgets (visible using "Show Contextual Help" from the Help menu).
  Use this to hook into the contextual help system in your extension.`);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.48d46625a03ec356bfc7.js.map