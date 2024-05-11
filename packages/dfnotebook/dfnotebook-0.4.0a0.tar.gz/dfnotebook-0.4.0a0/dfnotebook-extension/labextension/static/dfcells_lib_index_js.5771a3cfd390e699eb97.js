"use strict";
(self["webpackChunk_dfnotebook_dfnotebook_extension"] = self["webpackChunk_dfnotebook_dfnotebook_extension"] || []).push([["dfcells_lib_index_js"],{

/***/ "../dfcells/lib/index.js":
/*!*******************************!*\
  !*** ../dfcells/lib/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowAttachmentsCell": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.DataflowAttachmentsCell),
/* harmony export */   "DataflowAttachmentsCellModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.DataflowAttachmentsCellModel),
/* harmony export */   "DataflowCell": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.DataflowCell),
/* harmony export */   "DataflowCellModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.DataflowCellModel),
/* harmony export */   "DataflowCodeCell": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.DataflowCodeCell),
/* harmony export */   "DataflowCodeCellModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.DataflowCodeCellModel),
/* harmony export */   "DataflowInputArea": () => (/* reexport safe */ _inputarea__WEBPACK_IMPORTED_MODULE_0__.DataflowInputArea),
/* harmony export */   "DataflowInputPrompt": () => (/* reexport safe */ _inputarea__WEBPACK_IMPORTED_MODULE_0__.DataflowInputPrompt),
/* harmony export */   "DataflowMarkdownCell": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.DataflowMarkdownCell),
/* harmony export */   "DataflowMarkdownCellModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.DataflowMarkdownCellModel),
/* harmony export */   "DataflowRawCell": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.DataflowRawCell),
/* harmony export */   "DataflowRawCellModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.DataflowRawCellModel)
/* harmony export */ });
/* harmony import */ var _inputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./inputarea */ "../dfcells/lib/inputarea.js");
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "../dfcells/lib/model.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "../dfcells/lib/widget.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module dfcells
 */



//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../dfcells/lib/inputarea.js":
/*!***********************************!*\
  !*** ../dfcells/lib/inputarea.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowInputArea": () => (/* binding */ DataflowInputArea),
/* harmony export */   "DataflowInputPrompt": () => (/* binding */ DataflowInputPrompt)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);

const INPUT_TAG_CLASS = 'df-InputPrompt-tag';
class DataflowInputArea extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.InputArea {
    // kind of annoying as model still needs to be set later
    constructor(options) {
        super(Object.assign({ contentFactory: DataflowInputArea.defaultContentFactory }, options));
        this.prompt.model = this.model;
    }
    get prompt() {
        //@ts-ignore
        return this._prompt;
    }
    set prompt(value) {
        value.model = this.model;
        //@ts-ignore
        this._prompt = value;
    }
    addTag(value) {
        var _a;
        (_a = this.model) === null || _a === void 0 ? void 0 : _a.metadata.set('tag', value);
        this.prompt.updatePromptNode(this.prompt.executionCount);
    }
}
(function (DataflowInputArea) {
    class ContentFactory extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.InputArea.ContentFactory {
        /**
         * Create an input prompt.
         */
        createInputPrompt() {
            return new DataflowInputPrompt();
        }
    }
    DataflowInputArea.ContentFactory = ContentFactory;
    DataflowInputArea.defaultContentFactory = new ContentFactory({});
})(DataflowInputArea || (DataflowInputArea = {}));
class DataflowInputPrompt extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.InputPrompt {
    constructor(model = null) {
        super();
        this.model = model;
    }
    updatePromptNode(value) {
        var _a;
        if ((_a = this.model) === null || _a === void 0 ? void 0 : _a.metadata.get('tag')) {
            this.node.textContent = `[${this.model.metadata.get('tag')}]:`;
            this.addClass(INPUT_TAG_CLASS);
        }
        else if (value === null) {
            this.node.textContent = ' ';
            this.removeClass(INPUT_TAG_CLASS);
        }
        else {
            this.node.textContent = `[${value || ' '}]:`;
            this.removeClass(INPUT_TAG_CLASS);
        }
    }
    /**
     * The execution count for the prompt.
     */
    get executionCount() {
        return super.executionCount;
    }
    set executionCount(value) {
        super.executionCount = value;
        this.updatePromptNode(value);
    }
    get model() {
        return this._model;
    }
    set model(value) {
        this._model = value;
        if (this._model) {
            this.updatePromptNode(this.executionCount);
        }
    }
}
//# sourceMappingURL=inputarea.js.map

/***/ }),

/***/ "../dfcells/lib/model.js":
/*!*******************************!*\
  !*** ../dfcells/lib/model.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowAttachmentsCellModel": () => (/* binding */ DataflowAttachmentsCellModel),
/* harmony export */   "DataflowCellModel": () => (/* binding */ DataflowCellModel),
/* harmony export */   "DataflowCodeCellModel": () => (/* binding */ DataflowCodeCellModel),
/* harmony export */   "DataflowMarkdownCellModel": () => (/* binding */ DataflowMarkdownCellModel),
/* harmony export */   "DataflowRawCellModel": () => (/* binding */ DataflowRawCellModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);

// import { IOutputAreaModel } from "@jupyterlab/outputarea";
// import { JSONObject } from "@lumino/coreutils";
// type GConstructor<T = {}> = new (...args: any[]) => T;
// //type GConstructor<T = {}> = new (options: CellModel.IOptions) => T;
// type CellModelLike = GConstructor<CellModel>;
// function SetIdMixin<T extends CellModelLike>(Base: T) {
//     return class DataflowCellModelBase extends Base {
//         constructor(...args: any[]) {
//             super(args[0]);
//             const metadata = this.modelDB.getValue('metadata') as JSONObject;
//             metadata['dfnotebook'] = {};
//             metadata['dfnotebook']['id'] = this.id;
//         }
//     }
// }
// const DataflowCellModel = SetIdMixin(CellModel);
// const DataflowCodeCellModel = SetIdMixin(CodeCellModel);
// export { DataflowCellModel, DataflowCodeCellModel};
function setId(model) {
    // FIXME don't need this???
    //
    // const metadata = model.modelDB.getValue('metadata') as JSONObject;
    // metadata['dfnotebook'] = {};
    // metadata['dfnotebook']['id'] = model.id;
}
class DataflowCellModel extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CellModel {
    constructor(options) {
        super(options);
        setId(this);
    }
}
class DataflowAttachmentsCellModel extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.AttachmentsCellModel {
    constructor(options) {
        super(options);
        setId(this);
    }
}
class DataflowRawCellModel extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.RawCellModel {
    constructor(options) {
        super(options);
        setId(this);
    }
}
class DataflowMarkdownCellModel extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCellModel {
    constructor(options) {
        super(options);
        setId(this);
    }
}
class DataflowCodeCellModel extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCellModel {
    constructor(options) {
        super(options);
        setId(this);
    }
}
// export namespace DataflowCodeCellModel {
//   /**
//    * The default implementation of an `IContentFactory`.
//    */
//    export class ContentFactory extends CodeCellModel.ContentFactory {
//     /**
//      * Create an output area.
//      */
//     createOutputArea(options: IOutputAreaModel.IOptions): IOutputAreaModel {
//       return new OutputAreaModel(options);
//     }
//   }
//   /**
//    * The shared `ContentFactory` instance.
//    */
//   export const defaultContentFactory = new ContentFactory();
// }
//# sourceMappingURL=model.js.map

/***/ }),

/***/ "../dfcells/lib/widget.js":
/*!********************************!*\
  !*** ../dfcells/lib/widget.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowAttachmentsCell": () => (/* binding */ DataflowAttachmentsCell),
/* harmony export */   "DataflowCell": () => (/* binding */ DataflowCell),
/* harmony export */   "DataflowCodeCell": () => (/* binding */ DataflowCodeCell),
/* harmony export */   "DataflowMarkdownCell": () => (/* binding */ DataflowMarkdownCell),
/* harmony export */   "DataflowRawCell": () => (/* binding */ DataflowRawCell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _inputarea__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./inputarea */ "../dfcells/lib/inputarea.js");
/* harmony import */ var _dfnotebook_dfoutputarea__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @dfnotebook/dfoutputarea */ "../dfoutputarea/lib/widget.js");



/**
 * The CSS class added to the cell input area.
 */
const CELL_INPUT_AREA_CLASS = 'jp-Cell-inputArea';
/**
* The CSS class added to the cell output area.
*/
const CELL_OUTPUT_AREA_CLASS = 'jp-Cell-outputArea';
function setInputArea(cell, options) {
    // FIXME may be able to get panel via (this.layout as PanelLayout).widgets?
    //@ts-expect-error
    const panel = cell._inputWrapper;
    const input = cell.inputArea;
    // find the input area widget
    const { id } = input;
    let input_idx = -1;
    panel.widgets.forEach((widget, idx) => {
        if (widget.id === id) {
            input_idx = idx;
        }
    });
    const dfInput = new _inputarea__WEBPACK_IMPORTED_MODULE_1__.DataflowInputArea({
        model: cell.model,
        contentFactory: cell.contentFactory,
        updateOnShow: options.updateEditorOnShow,
        placeholder: options.placeholder
    });
    dfInput.addClass(CELL_INPUT_AREA_CLASS);
    panel.insertWidget(input_idx, dfInput);
    input.dispose();
    //@ts-expect-error
    cell._input = dfInput;
}
function setOutputArea(cell, options) {
    //@ts-expect-error
    const panel = cell._outputWrapper;
    const output = cell.outputArea;
    // find the output area widget
    const { id } = output;
    let output_idx = -1;
    panel.widgets.forEach((widget, idx) => {
        if (widget.id === id) {
            output_idx = idx;
        }
    });
    const dfOutput = new _dfnotebook_dfoutputarea__WEBPACK_IMPORTED_MODULE_2__.DataflowOutputArea({
        model: cell.model.outputs,
        rendermime: options.rendermime,
        contentFactory: cell.contentFactory,
        maxNumberOutputs: options.maxNumberOutputs
    }, 
    // FIXME move this to a function to unify with the code below and in dfnotebook/actions.tsx  
    cell.model.id.replace(/-/g, '').substring(0, 8));
    dfOutput.addClass(CELL_OUTPUT_AREA_CLASS);
    output.outputLengthChanged.disconnect(
    //@ts-expect-error
    cell._outputLengthHandler, cell);
    //@ts-expect-error
    dfOutput.outputLengthChanged.connect(cell._outputLengthHandler, cell);
    panel.insertWidget(output_idx, dfOutput);
    output.dispose();
    //@ts-expect-error
    cell._output = dfOutput;
}
class DataflowCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.Cell {
    constructor(options) {
        super(Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
        setInputArea(this, Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
    }
}
(function (DataflowCell) {
    class ContentFactory extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.Cell.ContentFactory {
        /**
         * Create an input prompt.
         */
        createInputPrompt() {
            return new _inputarea__WEBPACK_IMPORTED_MODULE_1__.DataflowInputPrompt();
        }
        /**
         * Create the output prompt for the widget.
         */
        createOutputPrompt() {
            return new _dfnotebook_dfoutputarea__WEBPACK_IMPORTED_MODULE_2__.DataflowOutputPrompt();
        }
    }
    DataflowCell.ContentFactory = ContentFactory;
})(DataflowCell || (DataflowCell = {}));
class DataflowMarkdownCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.MarkdownCell {
    constructor(options) {
        super(Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
        setInputArea(this, Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
    }
}
class DataflowRawCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.RawCell {
    constructor(options) {
        super(Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
        setInputArea(this, Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
    }
}
class DataflowAttachmentsCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.AttachmentsCell {
    constructor(options) {
        super(Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
        setInputArea(this, Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
    }
}
class DataflowCodeCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell {
    constructor(options) {
        super(Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
        setInputArea(this, Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
        setOutputArea(this, Object.assign({ contentFactory: DataflowCell.defaultContentFactory }, options));
    }
    setPromptToId() {
        // FIXME move this to a function to unify with the code in dfnotebook/actions.tsx
        this.setPrompt(`${this.model.id.replace(/-/g, '').substring(0, 8) || ''}`);
    }
    initializeState() {
        super.initializeState();
        this.setPromptToId();
        return this;
    }
    onStateChanged(model, args) {
        super.onStateChanged(model, args);
        switch (args.name) {
            case 'executionCount':
                this.setPromptToId();
                break;
            default:
                break;
        }
    }
}
(function (DataflowCodeCell) {
    /**
      * Execute a cell given a client session.
      */
    async function execute(cell, sessionContext, metadata, dfData, cellIdWidgetMap) {
        var _a;
        const model = cell.model;
        const code = model.value.text;
        if (!code.trim() || !((_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
            model.clearExecution();
            return;
        }
        const cellId = { cellId: model.id };
        metadata = Object.assign(Object.assign(Object.assign({}, model.metadata.toJSON()), metadata), cellId);
        const { recordTiming } = metadata;
        model.clearExecution();
        cell.outputHidden = false;
        cell.setPrompt('*');
        model.trusted = true;
        let future;
        try {
            const msgPromise = _dfnotebook_dfoutputarea__WEBPACK_IMPORTED_MODULE_2__.DataflowOutputArea.execute(code, cell.outputArea, sessionContext, metadata, dfData, cellIdWidgetMap);
            // cell.outputArea.future assigned synchronously in `execute`
            if (recordTiming) {
                const recordTimingHook = (msg) => {
                    let label;
                    switch (msg.header.msg_type) {
                        case 'status':
                            label = `status.${msg.content.execution_state}`;
                            break;
                        case 'execute_input':
                            label = 'execute_input';
                            break;
                        default:
                            return true;
                    }
                    // If the data is missing, estimate it to now
                    // Date was added in 5.1: https://jupyter-client.readthedocs.io/en/stable/messaging.html#message-header
                    const value = msg.header.date || new Date().toISOString();
                    const timingInfo = Object.assign({}, model.metadata.get('execution'));
                    timingInfo[`iopub.${label}`] = value;
                    model.metadata.set('execution', timingInfo);
                    return true;
                };
                cell.outputArea.future.registerMessageHook(recordTimingHook);
            }
            else {
                model.metadata.delete('execution');
            }
            const clearOutput = (msg) => {
                switch (msg.header.msg_type) {
                    case 'execute_input':
                        const executionCount = msg.content
                            .execution_count;
                        if (executionCount !== null) {
                            const cellId = executionCount.toString(16).padStart(8, '0');
                            if (cellIdWidgetMap) {
                                const cellWidget = cellIdWidgetMap[cellId];
                                cellWidget.model.value.text = msg.content.code;
                                const outputArea = cellWidget.outputArea;
                                outputArea.model.clear();
                            }
                        }
                        break;
                    default:
                        return true;
                }
                return true;
            };
            cell.outputArea.future.registerMessageHook(clearOutput);
            // Save this execution's future so we can compare in the catch below.
            future = cell.outputArea.future;
            const msg = (await msgPromise);
            model.executionCount = msg.content.execution_count;
            if (recordTiming) {
                const timingInfo = Object.assign({}, model.metadata.get('execution'));
                const started = msg.metadata.started;
                // Started is not in the API, but metadata IPyKernel sends
                if (started) {
                    timingInfo['shell.execute_reply.started'] = started;
                }
                // Per above, the 5.0 spec does not assume date, so we estimate is required
                const finished = msg.header.date;
                timingInfo['shell.execute_reply'] =
                    finished || new Date().toISOString();
                model.metadata.set('execution', timingInfo);
            }
            return msg;
        }
        catch (e) {
            // If we started executing, and the cell is still indicating this
            // execution, clear the prompt.
            if (future && !cell.isDisposed && cell.outputArea.future === future) {
                // cell.setPrompt('');
                // FIXME is this necessary?
                cell.setPromptToId();
                // cell.setPrompt(`${cell.model.id.substring(0, 8) || ''}`);
            }
            throw e;
        }
    }
    DataflowCodeCell.execute = execute;
})(DataflowCodeCell || (DataflowCodeCell = {}));
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "../dfoutputarea/lib/widget.js":
/*!*************************************!*\
  !*** ../dfoutputarea/lib/widget.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DataflowOutputArea": () => (/* binding */ DataflowOutputArea),
/* harmony export */   "DataflowOutputPrompt": () => (/* binding */ DataflowOutputPrompt)
/* harmony export */ });
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);

const OUTPUT_TAG_CLASS = 'df-OutputArea-tag';
class DataflowOutputArea extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputArea {
    constructor(options, cellId) {
        super(Object.assign({ contentFactory: DataflowOutputArea.defaultContentFactory }, options));
        this.onIOPub = (msg) => {
            const msgType = msg.header.msg_type;
            let output;
            switch (msgType) {
                case 'execute_result':
                case 'display_data':
                case 'stream':
                case 'error':
                    output = Object.assign(Object.assign({}, msg.content), { output_type: msgType });
                    if (output.execution_count) {
                        const cellId = output.execution_count.toString(16).padStart(8, '0');
                        if (msgType === 'stream') {
                            delete output.execution_count;
                        }
                        if (cellId !== this.cellId) {
                            if (DataflowOutputArea.cellIdWidgetMap) {
                                const cellWidget = DataflowOutputArea.cellIdWidgetMap[cellId];
                                //@ts-ignore
                                const outputArea = cellWidget._output;
                                outputArea._onIOPub(msg);
                            }
                            break;
                        }
                    }
                    //@ts-ignore
                    this._onIOPub(msg);
                    break;
                default: {
                    //@ts-ignore
                    this._onIOPub(msg);
                    break;
                }
            }
        };
        this.cellId = cellId;
    }
    get future() {
        return super.future;
    }
    set future(value) {
        super.future = value;
        super.future.onIOPub = this.onIOPub;
    }
    createOutputItem(model) {
        const panel = super.createOutputItem(model);
        if (panel) {
            if (model.metadata['output_tag']) {
                const prompt = panel.widgets[0];
                prompt.outputTag = model.metadata['output_tag'];
            }
        }
        return panel;
    }
}
class DataflowOutputPrompt extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputPrompt {
    constructor() {
        super(...arguments);
        this._outputTag = '';
    }
    updatePrompt() {
        if (this._outputTag) {
            this.node.textContent = `${this._outputTag}:`;
            this.addClass(OUTPUT_TAG_CLASS);
        }
        else if (this.executionCount === null) {
            this.node.textContent = '';
            this.removeClass(OUTPUT_TAG_CLASS);
        }
        else {
            const cellId = this.executionCount
                .toString(16)
                .padStart(8, '0');
            // .substr(0, 3);
            this.node.textContent = `[${cellId}]:`;
            this.removeClass(OUTPUT_TAG_CLASS);
        }
    }
    get executionCount() {
        return super.executionCount;
    }
    set executionCount(value) {
        super.executionCount = value;
        this.updatePrompt();
    }
    get outputTag() {
        return this._outputTag;
    }
    set outputTag(value) {
        this._outputTag = value;
        this.updatePrompt();
    }
}
(function (DataflowOutputArea) {
    async function execute(code, output, sessionContext, metadata, dfData, cellIdWidgetMap) {
        var _a;
        // Override the default for `stop_on_error`.
        let stopOnError = true;
        if (metadata &&
            Array.isArray(metadata.tags) &&
            metadata.tags.indexOf('raises-exception') !== -1) {
            stopOnError = false;
        }
        if (dfData === undefined) {
            // FIXME not sure if this works or not...
            dfData = {};
        }
        const content = {
            code,
            stop_on_error: stopOnError,
            user_expressions: { __dfkernel_data__: dfData }
        };
        const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            throw new Error('Session has no kernel.');
        }
        const future = kernel.requestExecute(content, false, metadata);
        output.future = future;
        DataflowOutputArea.cellIdWidgetMap = cellIdWidgetMap;
        return future.done;
    }
    DataflowOutputArea.execute = execute;
    /**
     * The default implementation of `IContentFactory`.
     */
    class ContentFactory extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputArea.ContentFactory {
        /**
         * Create the output prompt for the widget.
         */
        createOutputPrompt() {
            return new DataflowOutputPrompt();
        }
    }
    DataflowOutputArea.ContentFactory = ContentFactory;
    DataflowOutputArea.defaultContentFactory = new ContentFactory();
})(DataflowOutputArea || (DataflowOutputArea = {}));
//# sourceMappingURL=widget.js.map

/***/ })

}]);
//# sourceMappingURL=dfcells_lib_index_js.5771a3cfd390e699eb97.js.map