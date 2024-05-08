"use strict";
(self["webpackChunkpretzelai"] = self["webpackChunkpretzelai"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var monaco_editor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! monaco-editor */ "webpack/sharing/consume/default/monaco-editor/monaco-editor");
/* harmony import */ var monaco_editor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(monaco_editor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var openai__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! openai */ "webpack/sharing/consume/default/openai/openai");
/* harmony import */ var openai__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(openai__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _azure_openai__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @azure/openai */ "webpack/sharing/consume/default/@azure/openai/@azure/openai");
/* harmony import */ var _azure_openai__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_azure_openai__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _prompt__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./prompt */ "./lib/prompt.js");
/* harmony import */ var posthog_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! posthog-js */ "webpack/sharing/consume/default/posthog-js/posthog-js");
/* harmony import */ var posthog_js__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(posthog_js__WEBPACK_IMPORTED_MODULE_6__);









posthog_js__WEBPACK_IMPORTED_MODULE_6___default().init('phc_FnIUQkcrbS8sgtNFHp5kpMkSvL5ydtO1nd9mPllRQqZ', {
    api_host: 'https://d2yfaqny8nshvd.cloudfront.net'
});
const PLUGIN_ID = 'pretzelai:plugin';
const NUMBER_OF_SIMILAR_CELLS = 3;
const extension = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    activate: async (app, palette, notebookTracker, settingRegistry) => {
        const { commands } = app;
        const command = 'pretzelai:replace-code';
        const placeholderDisabled = 'To use AI features, please set your OpenAI API key or Azure API details in the Pretzel AI Settings.\n' +
            'You can also use the free Pretzel AI server.\n' +
            'Go To: Settings > Settings Editor > Pretzel AI Settings to configure';
        const placeHolderEnabled = 'Ask AI. Use @variableName to refernce defined variables and dataframes';
        let openAiApiKey = '';
        let openAiBaseUrl = '';
        let aiService = 'Use Pretzel AI Server';
        let azureBaseUrl = '';
        let azureDeploymentName = '';
        let azureApiKey = '';
        let openai;
        // Function to load settings
        function loadSettings(updateFunc) {
            settingRegistry
                .load(extension.id)
                .then(settings => {
                openAiApiKey = settings.get('openAiSettings').composite
                    .openAiApiKey;
                aiService = settings.get('aiService').composite;
                openAiBaseUrl = settings.get('openAiSettings').composite
                    .openAiBaseUrl;
                azureBaseUrl = settings.get('azureSettings').composite
                    .azureBaseUrl;
                azureDeploymentName = settings.get('azureSettings').composite
                    .azureDeploymentName;
                azureApiKey = settings.get('azureSettings').composite
                    .azureApiKey;
                updateFunc === null || updateFunc === void 0 ? void 0 : updateFunc();
            })
                .catch(reason => {
                console.error('Failed to load settings for Pretzel', reason);
            });
        }
        loadSettings();
        function loadOpenai() {
            if (openAiApiKey) {
                openai = new (openai__WEBPACK_IMPORTED_MODULE_3___default())({
                    apiKey: openAiApiKey,
                    dangerouslyAllowBrowser: true
                });
            }
            else {
                setTimeout(loadOpenai, 1000);
            }
        }
        loadOpenai();
        // Listen for future changes in settings
        settingRegistry.pluginChanged.connect((sender, plugin) => {
            if (plugin === extension.id) {
                const updateFunc = async () => {
                    const submitButton = document.querySelector('.pretzelInputSubmitButton');
                    const inputField = document.querySelector('.pretzelInputField');
                    if (submitButton) {
                        if ((aiService === 'OpenAI API key' && openAiApiKey) ||
                            aiService === 'Use Pretzel AI Server' ||
                            (aiService === 'Use Azure API' &&
                                azureBaseUrl &&
                                azureDeploymentName &&
                                azureApiKey)) {
                            submitButton.disabled = false;
                            inputField.placeholder = placeHolderEnabled;
                        }
                        else {
                            submitButton.disabled = true;
                            inputField.placeholder =
                                placeholderDisabled;
                        }
                    }
                };
                loadSettings(updateFunc);
            }
        });
        let embeddings;
        async function createEmbeddings(embeddingsJSON, cells, path) {
            embeddings = embeddingsJSON;
            const newEmbeddingsArray = [];
            const promises = cells.map(cell => {
                return (async () => {
                    const index = embeddings.findIndex(e => e.id === cell.id);
                    if (index !== -1) {
                        const hash = await (0,_utils__WEBPACK_IMPORTED_MODULE_7__.calculateHash)(cell.source);
                        if (hash !== embeddings[index].hash) {
                            try {
                                const response = await (0,_prompt__WEBPACK_IMPORTED_MODULE_8__.openaiEmbeddings)(cell.source, aiService, openai);
                                newEmbeddingsArray.push({
                                    id: cell.id,
                                    source: cell.source,
                                    hash,
                                    embedding: response.data[0].embedding
                                });
                            }
                            catch (error) {
                                console.error('Error generating embedding:', error);
                            }
                        }
                        else {
                            newEmbeddingsArray.push(embeddings[index]);
                        }
                    }
                    else {
                        try {
                            const response = await (0,_prompt__WEBPACK_IMPORTED_MODULE_8__.openaiEmbeddings)(cell.source, aiService, openai);
                            const hash = await (0,_utils__WEBPACK_IMPORTED_MODULE_7__.calculateHash)(cell.source);
                            newEmbeddingsArray.push({
                                id: cell.id,
                                source: cell.source,
                                hash,
                                embedding: response.data[0].embedding
                            });
                        }
                        catch (error) {
                            console.error('Error generating embedding:', error);
                        }
                    }
                })();
            });
            await Promise.allSettled(promises);
            const oldSet = new Set(embeddings.map(e => e.hash));
            const newSet = new Set(newEmbeddingsArray.map(e => e.hash));
            if (!(0,_utils__WEBPACK_IMPORTED_MODULE_7__.isSetsEqual)(oldSet, newSet)) {
                app.serviceManager.contents.save(path, {
                    type: 'file',
                    format: 'text',
                    content: JSON.stringify(newEmbeddingsArray)
                });
            }
        }
        // Function to print the source of all cells once the notebook is defined
        function getEmbeddings() {
            const notebook = notebookTracker.currentWidget;
            if (notebook === null || notebook === void 0 ? void 0 : notebook.model) {
                const currentNotebookPath = notebook.context.path;
                const embeddingsPath = currentNotebookPath.replace('.ipynb', '') + '_embeddings.json';
                app.serviceManager.contents
                    .get(embeddingsPath)
                    .then(file => {
                    try {
                        const embJSON = JSON.parse(file.content);
                        createEmbeddings(embJSON, notebook.model.sharedModel.cells, embeddingsPath);
                    }
                    catch (error) {
                        console.error('Error parsing embeddings JSON:', error);
                    }
                })
                    .catch(async (error) => {
                    createEmbeddings([], notebook.model.sharedModel.cells, embeddingsPath);
                });
                // Temporary solution to keep refreshing hashes in non blocking thread
                setTimeout(getEmbeddings, 1000);
            }
            else {
                setTimeout(getEmbeddings, 1000);
            }
        }
        getEmbeddings();
        async function getVariableValue(variableName) {
            var _a;
            const notebook = notebookTracker.currentWidget;
            if (notebook && ((_a = notebook.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
                const kernel = notebook.sessionContext.session.kernel;
                try {
                    // get the type - if dataframe, we get columns
                    // if other, we get the string representation
                    const executeRequest = kernel.requestExecute({
                        code: `print(${variableName})`
                    });
                    let variableValue = null;
                    // Registering a message hook to intercept messages
                    kernel.registerMessageHook(executeRequest.msg.header.msg_id, (msg) => {
                        if (msg.header.msg_type === 'stream' &&
                            // @ts-expect-error tserror
                            msg.content.name === 'stdout') {
                            // @ts-expect-error tserror
                            variableValue = msg.content.text.trim();
                        }
                        return true;
                    });
                    // Await the completion of the execute request
                    const reply = await executeRequest.done;
                    if (reply && reply.content.status === 'ok') {
                        return variableValue;
                    }
                    else {
                        console.error('Failed to retrieve variable value');
                        return null;
                    }
                }
                catch (error) {
                    console.error('Error retrieving variable value:', error);
                    return null;
                }
            }
            else {
                console.error('No active kernel found');
                return null;
            }
        }
        commands.addCommand(command, {
            label: 'Replace Cell Code',
            execute: () => {
                const activeCell = notebookTracker.activeCell;
                if (activeCell) {
                    // Cmd K twice should toggle the box
                    // Check if an existing div with ID pretzelParentContainerAI exists on activeCell.node
                    const existingDiv = activeCell.node.querySelector('.pretzelParentContainerAI');
                    if (existingDiv) {
                        // If so, delete that div
                        existingDiv.remove();
                        // Switch focus back to the Jupyter cell
                        activeCell.editor.focus();
                        return;
                    }
                    const oldCode = activeCell.model.sharedModel.source;
                    // Create a parent container for all dynamically created elements
                    const parentContainer = document.createElement('div');
                    parentContainer.classList.add('pretzelParentContainerAI');
                    activeCell.node.appendChild(parentContainer);
                    // Create an input field and append it below the cell
                    const inputContainer = document.createElement('div');
                    inputContainer.style.marginTop = '10px';
                    inputContainer.style.marginLeft = '70px';
                    inputContainer.style.display = 'flex';
                    inputContainer.style.flexDirection = 'column';
                    parentContainer.appendChild(inputContainer);
                    const inputField = document.createElement('textarea');
                    inputField.classList.add('pretzelInputField');
                    inputField.placeholder = placeHolderEnabled;
                    inputField.style.width = '100%';
                    inputField.style.height = '100px';
                    inputContainer.appendChild(inputField);
                    inputField.addEventListener('keydown', event => {
                        if (event.key === 'Escape') {
                            // TODO: this doesn't work - the Escape key isn't being captured
                            // but every other key press is being captured
                            event.preventDefault(); // Prevent any default behavior
                            // Shift focus back to the editor of the active cell
                            const activeCell = notebookTracker.activeCell;
                            if (activeCell && activeCell.editor) {
                                activeCell.editor.focus(); // Focus the editor of the active cell
                            }
                        }
                        // handle enter key press to trigger submit
                        if (event.key === 'Enter') {
                            event.preventDefault();
                            if (!submitButton.disabled) {
                                handleSubmit();
                            }
                        }
                    });
                    const callingP = document.createElement('p');
                    callingP.textContent = 'Calling AI Service...';
                    parentContainer.appendChild(callingP);
                    const inputFieldButtonsContainer = document.createElement('div');
                    inputFieldButtonsContainer.style.marginTop = '10px';
                    inputFieldButtonsContainer.style.display = 'flex';
                    inputFieldButtonsContainer.style.flexDirection = 'row';
                    inputContainer.appendChild(inputFieldButtonsContainer);
                    inputField.focus();
                    const submitButton = document.createElement('button');
                    submitButton.classList.add('pretzelInputSubmitButton');
                    submitButton.textContent = 'Submit';
                    submitButton.style.backgroundColor = 'lightblue';
                    submitButton.style.borderRadius = '5px';
                    submitButton.style.border = '1px solid darkblue';
                    submitButton.style.maxWidth = '100px';
                    submitButton.style.minHeight = '25px';
                    submitButton.style.marginTop = '10px';
                    submitButton.style.marginRight = '10px';
                    inputFieldButtonsContainer.appendChild(submitButton);
                    // write code to add a button the removed the inputField and submitButton
                    const removeButton = document.createElement('button');
                    removeButton.textContent = 'Remove';
                    removeButton.style.backgroundColor = 'lightcoral';
                    removeButton.style.borderRadius = '5px';
                    removeButton.style.border = '1px solid darkred';
                    removeButton.style.maxWidth = '100px';
                    removeButton.style.minHeight = '25px';
                    removeButton.style.marginTop = '10px';
                    inputFieldButtonsContainer.appendChild(removeButton);
                    removeButton.addEventListener('click', () => {
                        activeCell.node.removeChild(parentContainer);
                    });
                    if ((aiService === 'OpenAI API key' && !openAiApiKey) ||
                        (aiService === 'Use Azure API' &&
                            (!azureBaseUrl || !azureDeploymentName || !azureApiKey))) {
                        inputField.placeholder = placeholderDisabled;
                        submitButton.disabled = true;
                    }
                    const handleSubmit = async () => {
                        let userInput = inputField.value;
                        if (userInput !== '') {
                            parentContainer.removeChild(inputContainer);
                            let diffEditor = null;
                            const renderEditor = (gen) => {
                                try {
                                    if (!diffEditor) {
                                        createEditorComponents();
                                    }
                                    const modifiedModel = diffEditor.getModel().modified;
                                    const endLineNumber = modifiedModel.getLineCount();
                                    const endColumn = modifiedModel.getLineMaxColumn(endLineNumber);
                                    modifiedModel.applyEdits([
                                        {
                                            range: new monaco_editor__WEBPACK_IMPORTED_MODULE_2__.Range(endLineNumber, endColumn, endLineNumber, endColumn),
                                            text: gen,
                                            forceMoveMarkers: true
                                        }
                                    ]);
                                }
                                catch (error) {
                                    console.log('Error rendering editor:', error);
                                }
                            };
                            let diffButtonsContainer;
                            let acceptButton;
                            let rejectButton;
                            let editPromptButton;
                            const createEditorComponents = () => {
                                // generate the editor components
                                // first, top level container to hold all diff related items
                                const diffContainer = document.createElement('div');
                                diffContainer.style.marginTop = '10px';
                                diffContainer.style.display = 'flex';
                                diffContainer.style.flexDirection = 'column';
                                parentContainer.appendChild(diffContainer);
                                // next, container to hold the diff editor
                                const diffEditorContainer = document.createElement('div');
                                diffEditorContainer.style.height = '200px';
                                diffContainer.appendChild(diffEditorContainer);
                                // finally, the diff editor itself
                                const currentTheme = document.body.getAttribute('data-jp-theme-light') === 'true'
                                    ? 'vs'
                                    : 'vs-dark';
                                diffEditor = monaco_editor__WEBPACK_IMPORTED_MODULE_2__.editor.createDiffEditor(diffEditorContainer, {
                                    readOnly: true,
                                    theme: currentTheme
                                });
                                diffEditor.setModel({
                                    original: monaco_editor__WEBPACK_IMPORTED_MODULE_2__.editor.createModel(oldCode, 'python'),
                                    modified: monaco_editor__WEBPACK_IMPORTED_MODULE_2__.editor.createModel('', 'python')
                                });
                                diffButtonsContainer = document.createElement('div');
                                diffButtonsContainer.style.marginTop = '10px';
                                diffButtonsContainer.style.marginLeft = '70px';
                                diffButtonsContainer.style.display = 'flex';
                                diffButtonsContainer.style.flexDirection = 'row';
                                diffContainer.appendChild(diffButtonsContainer);
                                // Create "Accept" and "Reject" buttons
                                acceptButton = document.createElement('button');
                                acceptButton.textContent = 'Accept';
                                acceptButton.style.backgroundColor = 'lightblue';
                                acceptButton.style.borderRadius = '5px';
                                acceptButton.style.border = '1px solid darkblue';
                                acceptButton.style.maxWidth = '100px';
                                acceptButton.style.minHeight = '25px';
                                acceptButton.style.marginRight = '10px';
                                acceptButton.addEventListener('click', () => {
                                    const modifiedCode = diffEditor
                                        .getModel()
                                        .modified.getValue();
                                    activeCell.model.sharedModel.source = modifiedCode;
                                    commands.execute('notebook:run-cell');
                                    activeCell.node.removeChild(parentContainer);
                                });
                                rejectButton = document.createElement('button');
                                rejectButton.textContent = 'Reject';
                                rejectButton.style.backgroundColor = 'lightblue';
                                rejectButton.style.borderRadius = '5px';
                                rejectButton.style.border = '1px solid darkblue';
                                rejectButton.style.maxWidth = '100px';
                                rejectButton.style.minHeight = '25px';
                                rejectButton.style.marginRight = '10px';
                                rejectButton.addEventListener('click', () => {
                                    activeCell.node.removeChild(parentContainer);
                                    activeCell.model.sharedModel.source = oldCode;
                                });
                                editPromptButton = document.createElement('button');
                                editPromptButton.textContent = 'Edit Prompt';
                                editPromptButton.style.backgroundColor = 'lightblue';
                                editPromptButton.style.borderRadius = '5px';
                                editPromptButton.style.border = '1px solid darkblue';
                                editPromptButton.style.maxWidth = '100px';
                                editPromptButton.style.minHeight = '25px';
                                editPromptButton.style.marginRight = '10px';
                                editPromptButton.addEventListener('click', () => {
                                    parentContainer.removeChild(diffContainer);
                                    parentContainer.appendChild(inputContainer);
                                    diffEditor = null;
                                });
                                // Handle Enter key press to trigger accept on accept/reject buttons
                                diffButtonsContainer.addEventListener('keydown', event => {
                                    if (event.key === 'Enter') {
                                        event.preventDefault();
                                        const activeElement = document.activeElement;
                                        if (activeElement === acceptButton) {
                                            acceptButton.click();
                                        }
                                        else if (activeElement === rejectButton) {
                                            rejectButton.click();
                                        }
                                    }
                                });
                                // Handle Escape key press to trigger reject on accept/reject buttons
                                diffButtonsContainer.addEventListener('keydown', event => {
                                    if (event.key === 'Escape') {
                                        event.preventDefault();
                                        rejectButton.click();
                                    }
                                });
                            };
                            const variablePattern = /@(\w+)/g;
                            let match;
                            let modifiedUserInput = userInput;
                            while ((match = variablePattern.exec(userInput)) !== null) {
                                try {
                                    const variableName = match[1];
                                    // get value of var using the getVariableValue function
                                    const variableType = await getVariableValue(`type(${variableName})`);
                                    // check if variableType is dataframe
                                    // if it is, get columns and add to modifiedUserInput
                                    if (variableType === null || variableType === void 0 ? void 0 : variableType.includes('DataFrame')) {
                                        const variableColumns = await getVariableValue(`${variableName}.columns`);
                                        modifiedUserInput += `\n${variableName} is a dataframe with the following columns: ${variableColumns}\n`;
                                    }
                                    else if (variableType) {
                                        const variableValue = await getVariableValue(variableName);
                                        modifiedUserInput += `\nPrinting ${variableName} in Python returns the string ${variableValue}\n`;
                                    }
                                }
                                catch (error) {
                                    console.error(`Error accessing variable ${match[1]}:`, error);
                                }
                            }
                            userInput = modifiedUserInput;
                            if (aiService === 'OpenAI API key' && openAiApiKey) {
                                try {
                                    const openai = new (openai__WEBPACK_IMPORTED_MODULE_3___default())({
                                        apiKey: openAiApiKey,
                                        dangerouslyAllowBrowser: true,
                                        baseURL: openAiBaseUrl ? openAiBaseUrl : undefined
                                    });
                                    const complete = async () => {
                                        var _a, _b;
                                        const topSimilarities = await (0,_prompt__WEBPACK_IMPORTED_MODULE_8__.getTopSimilarities)(userInput, embeddings, NUMBER_OF_SIMILAR_CELLS, openai, aiService);
                                        const prompt = (0,_prompt__WEBPACK_IMPORTED_MODULE_8__.generatePrompt)(userInput, oldCode, topSimilarities);
                                        posthog_js__WEBPACK_IMPORTED_MODULE_6___default().capture('prompt', { property: userInput });
                                        const stream = await openai.chat.completions.create({
                                            model: 'gpt-4-turbo-preview',
                                            messages: [
                                                {
                                                    role: 'system',
                                                    content: _prompt__WEBPACK_IMPORTED_MODULE_8__.systemPrompt
                                                },
                                                {
                                                    role: 'user',
                                                    content: prompt
                                                }
                                            ],
                                            stream: true
                                        });
                                        for await (const chunk of stream) {
                                            renderEditor(((_b = (_a = chunk.choices[0]) === null || _a === void 0 ? void 0 : _a.delta) === null || _b === void 0 ? void 0 : _b.content) || '');
                                        }
                                    };
                                    complete();
                                }
                                catch (error) {
                                    activeCell.node.removeChild(parentContainer);
                                }
                            }
                            else if (aiService === 'Use Pretzel AI Server') {
                                const topSimilarities = await (0,_prompt__WEBPACK_IMPORTED_MODULE_8__.getTopSimilarities)(userInput, embeddings, NUMBER_OF_SIMILAR_CELLS, openai, aiService);
                                const options = {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({
                                        oldCode,
                                        userInput,
                                        topSimilarities
                                    })
                                };
                                posthog_js__WEBPACK_IMPORTED_MODULE_6___default().capture('prompt', { property: userInput });
                                try {
                                    const response = await fetch('https://wjwgjk52kb3trqnlqivqqyxm3i0glvof.lambda-url.eu-central-1.on.aws/', options);
                                    const reader = response.body.getReader();
                                    const decoder = new TextDecoder('utf-8');
                                    let isReading = true;
                                    while (isReading) {
                                        const { done, value } = await reader.read();
                                        if (done) {
                                            isReading = false;
                                        }
                                        const chunk = decoder.decode(value);
                                        renderEditor(chunk);
                                    }
                                    diffButtonsContainer.appendChild(acceptButton);
                                    diffButtonsContainer.appendChild(rejectButton);
                                    diffButtonsContainer.appendChild(editPromptButton);
                                }
                                catch (error) {
                                    activeCell.model.sharedModel.source = `# Error: ${error}\n${oldCode}`;
                                    activeCell.node.removeChild(parentContainer);
                                }
                            }
                            else if (aiService === 'Use Azure API' &&
                                azureBaseUrl &&
                                azureDeploymentName &&
                                azureApiKey) {
                                try {
                                    const client = new _azure_openai__WEBPACK_IMPORTED_MODULE_5__.OpenAIClient(azureBaseUrl, new _azure_openai__WEBPACK_IMPORTED_MODULE_5__.AzureKeyCredential(azureApiKey));
                                    const deploymentId = azureDeploymentName;
                                    const prompt = [
                                        `Write python code to do \n"""\n${userInput}\n"""\nThe previous code is\n"""\n${oldCode}\n"""\nReturn ONLY executable python code, no backticks`
                                    ];
                                    const result = await client.getCompletions(deploymentId, prompt);
                                    for (const choice of result.choices) {
                                        renderEditor(choice.text);
                                    }
                                }
                                catch (error) {
                                    activeCell.model.sharedModel.source = `# Error: ${error}\n${oldCode}`;
                                    activeCell.node.removeChild(parentContainer);
                                }
                            }
                        }
                    };
                    // Handle submit button click to trigger accept
                    submitButton.addEventListener('click', handleSubmit);
                }
            }
        });
        const category = 'Cell Operations';
        palette.addItem({ command, category });
        app.commands.addKeyBinding({
            command,
            keys: ['Accel K'],
            selector: '.jp-Notebook'
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/prompt.js":
/*!***********************!*\
  !*** ./lib/prompt.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   EMBEDDING_MODEL: () => (/* binding */ EMBEDDING_MODEL),
/* harmony export */   generatePrompt: () => (/* binding */ generatePrompt),
/* harmony export */   getTopSimilarities: () => (/* binding */ getTopSimilarities),
/* harmony export */   openaiEmbeddings: () => (/* binding */ openaiEmbeddings),
/* harmony export */   systemPrompt: () => (/* binding */ systemPrompt)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");

const EMBEDDING_MODEL = 'text-embedding-3-large';
function generatePrompt(userInput, oldCode, topSimilarities) {
    return `The user wants to do the following:
"""
${userInput}
"""

${oldCode
        ? `The following code already exists in the notebook cell:
"""
${oldCode}
"""

`
        : ''}
${topSimilarities.length > 0
        ? `We also have the following matching code chunks in the notebook\n---\n${topSimilarities.join('\n---\n')}\n---\n`
        : ''}
Based on the above, return ONLY executable python code, no backticks.`;
}
const openaiEmbeddings = async (source, aiService, openai) => {
    return aiService === 'Use Pretzel AI Server'
        ? (await (await fetch('https://e7l46ifvcg6qrbuinytg7u535y0denki.lambda-url.eu-central-1.on.aws/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source: source
            })
        })).json())
        : await openai.embeddings.create({
            model: EMBEDDING_MODEL,
            input: source
        });
};
const getTopSimilarities = async (userInput, embeddings, numberOfSimilarities, openai, aiService) => {
    const response = await openaiEmbeddings(userInput, aiService, openai);
    const userInputEmbedding = response.data[0].embedding;
    const similarities = embeddings.map(embedding => (0,_utils__WEBPACK_IMPORTED_MODULE_0__.cosineSimilarity)(embedding.embedding, userInputEmbedding));
    return similarities
        .map((value, index) => ({ value, index }))
        .sort((a, b) => b.value - a.value)
        .slice(0, numberOfSimilarities)
        .map(e => embeddings[e.index].source);
};
const systemPrompt = 'You are a helpful assistant that helps users write python code in Jupyter notebook cells. ' +
    'You are helping the user write new code and edit old code in Jupyter notebooks. ' +
    'You write code exactly as if an expert python user would write, reusing existing variables and functions as needed. ' +
    'You respond with the clean, good quality, working python code only, no backticks.';


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   calculateHash: () => (/* binding */ calculateHash),
/* harmony export */   cosineSimilarity: () => (/* binding */ cosineSimilarity),
/* harmony export */   isSetsEqual: () => (/* binding */ isSetsEqual)
/* harmony export */ });
async function calculateHash(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}
const cosineSimilarity = (vecA, vecB) => {
    const dotProduct = vecA.reduce((acc, current, index) => acc + current * vecB[index], 0);
    const magnitudeA = Math.sqrt(vecA.reduce((acc, val) => acc + val * val, 0));
    const magnitudeB = Math.sqrt(vecB.reduce((acc, val) => acc + val * val, 0));
    return dotProduct / (magnitudeA * magnitudeB);
};
const isSetsEqual = (xs, ys) => xs.size === ys.size && [...xs].every(x => ys.has(x));


/***/ })

}]);
//# sourceMappingURL=lib_index_js.8faf49368007ce724bc7.js.map