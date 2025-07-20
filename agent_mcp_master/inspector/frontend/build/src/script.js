import { io } from 'socket.io-client';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const connectBtn = document.getElementById('connect-btn');
    const agentCardUrlInput = document.getElementById('agent-card-url');
    const httpHeadersToggle = document.getElementById('http-headers-toggle');
    const httpHeadersContent = document.getElementById('http-headers-content');
    const headersList = document.getElementById('headers-list');
    const addHeaderBtn = document.getElementById('add-header-btn');
    const collapsibleHeader = document.querySelector('.collapsible-header');
    const collapsibleContent = document.querySelector('.collapsible-content');
    const agentCardCodeContent = document.getElementById('agent-card-content');
    const validationErrorsContainer = document.getElementById('validation-errors');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const debugConsole = document.getElementById('debug-console');
    const debugHandle = document.getElementById('debug-handle');
    const debugContent = document.getElementById('debug-content');
    const clearConsoleBtn = document.getElementById('clear-console-btn');
    const toggleConsoleBtn = document.getElementById('toggle-console-btn');
    const jsonModal = document.getElementById('json-modal');
    const modalJsonContent = document.getElementById('modal-json-content');
    const modalCloseBtn = document.querySelector('.modal-close-btn');
    let isResizing = false;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const rawLogStore = {};
    const messageJsonStore = {};
    debugHandle.addEventListener('mousedown', (e) => {
        const target = e.target;
        if (target === debugHandle || target.tagName === 'SPAN') {
            isResizing = true;
            document.body.style.userSelect = 'none';
            document.body.style.pointerEvents = 'none';
        }
    });
    window.addEventListener('mousemove', (e) => {
        if (!isResizing)
            return;
        const newHeight = window.innerHeight - e.clientY;
        if (newHeight > 40 && newHeight < window.innerHeight * 0.9) {
            debugConsole.style.height = `${newHeight}px`;
        }
    });
    window.addEventListener('mouseup', () => {
        isResizing = false;
        document.body.style.userSelect = '';
        document.body.style.pointerEvents = '';
    });
    collapsibleHeader.addEventListener('click', () => {
        collapsibleHeader.classList.toggle('collapsed');
        collapsibleContent.classList.toggle('collapsed');
    });
    // HTTP Headers toggle functionality
    httpHeadersToggle.addEventListener('click', () => {
        const isExpanded = httpHeadersContent.classList.toggle('expanded');
        const toggleIcon = httpHeadersToggle.querySelector('.toggle-icon');
        if (toggleIcon) {
            toggleIcon.textContent = isExpanded ? '▼' : '►';
        }
    });
    // Add a new, empty header field when the button is clicked
    addHeaderBtn.addEventListener('click', () => addHeaderField());
    headersList.addEventListener('click', event => {
        var _a;
        const removeBtn = event.target.closest('.remove-header-btn');
        if (removeBtn) {
            (_a = removeBtn.closest('.header-item')) === null || _a === void 0 ? void 0 : _a.remove();
        }
    });
    // Function to add a new header field
    function addHeaderField(name = '', value = '') {
        const headerItemHTML = `
      <div class="header-item">
        <input type="text" class="header-name" placeholder="Header Name" value="${name}">
        <input type="text" class="header-value" placeholder="Header Value" value="${value}">
        <button type="button" class="remove-header-btn" aria-label="Remove header">×</button>
      </div>
    `;
        headersList.insertAdjacentHTML('beforeend', headerItemHTML);
    }
    // Function to collect all headers
    function getCustomHeaders() {
        const headerItems = headersList.querySelectorAll('.header-item');
        return Array.from(headerItems).reduce((headers, item) => {
            const nameInput = item.querySelector('.header-name');
            const valueInput = item.querySelector('.header-value');
            const name = nameInput === null || nameInput === void 0 ? void 0 : nameInput.value.trim();
            const value = valueInput === null || valueInput === void 0 ? void 0 : valueInput.value.trim();
            // Only add the header if both name and value are present
            if (name && value) {
                headers[name] = value;
            }
            return headers;
        }, {});
    }
    clearConsoleBtn.addEventListener('click', () => {
        debugContent.innerHTML = '';
        Object.keys(rawLogStore).forEach(key => delete rawLogStore[key]);
    });
    toggleConsoleBtn.addEventListener('click', () => {
        const isHidden = debugConsole.classList.toggle('hidden');
        toggleConsoleBtn.textContent = isHidden ? 'Show' : 'Hide';
    });
    modalCloseBtn.addEventListener('click', () => jsonModal.classList.add('hidden'));
    jsonModal.addEventListener('click', (e) => {
        if (e.target === jsonModal) {
            jsonModal.classList.add('hidden');
        }
    });
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const showJsonInModal = (jsonData) => {
        if (jsonData) {
            let jsonString = JSON.stringify(jsonData, null, 2);
            jsonString = jsonString.replace(/"method": "([^"]+)"/g, '<span class="json-highlight">"method": "$1"</span>');
            modalJsonContent.innerHTML = jsonString;
            jsonModal.classList.remove('hidden');
        }
    };
    connectBtn.addEventListener('click', async () => {
        let agentCardUrl = agentCardUrlInput.value.trim();
        if (!agentCardUrl) {
            return alert('Please enter an agent card URL.');
        }
        if (!/^https?:\/\//i.test(agentCardUrl)) {
            agentCardUrl = 'http://' + agentCardUrl;
        }
        agentCardCodeContent.textContent = '';
        validationErrorsContainer.innerHTML =
            '<p class="placeholder-text">Fetching Agent Card...</p>';
        chatInput.disabled = true;
        sendBtn.disabled = true;
        // Get custom headers
        const customHeaders = getCustomHeaders();
        // Prepare request headers
        const requestHeaders = Object.assign({ 'Content-Type': 'application/json' }, customHeaders);
        try {
            const response = await fetch('/agent-card', {
                method: 'POST',
                headers: requestHeaders,
                body: JSON.stringify({ url: agentCardUrl, sid: socket.id }),
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }
            agentCardCodeContent.textContent = JSON.stringify(data.card, null, 2);
            if (window.hljs) {
                window.hljs.highlightElement(agentCardCodeContent);
            }
            else {
                console.warn('highlight.js not loaded. Syntax highlighting skipped.');
            }
            validationErrorsContainer.innerHTML =
                '<p class="placeholder-text">Initializing client session...</p>';
            socket.emit('initialize_client', {
                url: agentCardUrl,
                customHeaders: customHeaders,
            });
            if (data.validation_errors.length > 0) {
                validationErrorsContainer.innerHTML = `<h3>Validation Errors</h3><ul>${data.validation_errors.map((e) => `<li>${e}</li>`).join('')}</ul>`;
            }
            else {
                validationErrorsContainer.innerHTML =
                    '<p style="color: green;">Agent card is valid.</p>';
            }
        }
        catch (error) {
            validationErrorsContainer.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            chatInput.disabled = true;
            sendBtn.disabled = true;
        }
    });
    socket.on('client_initialized', (data) => {
        if (data.status === 'success') {
            chatInput.disabled = false;
            sendBtn.disabled = false;
            chatMessages.innerHTML =
                '<p class="placeholder-text">Ready to chat.</p>';
            debugContent.innerHTML = '';
            Object.keys(rawLogStore).forEach(key => delete rawLogStore[key]);
            Object.keys(messageJsonStore).forEach(key => delete messageJsonStore[key]);
        }
        else {
            validationErrorsContainer.innerHTML = `<p style="color: red;">Error initializing client: ${data.message}</p>`;
        }
    });
    let contextId = null;
    const sendMessage = () => {
        const messageText = chatInput.value;
        if (messageText.trim() && !chatInput.disabled) {
            const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
            appendMessage('user', messageText, messageId);
            socket.emit('send_message', {
                message: messageText,
                id: messageId,
                contextId,
            });
            chatInput.value = '';
        }
    };
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter')
            sendMessage();
    });
    socket.on('agent_response', (event) => {
        var _a, _b, _c, _d, _e, _f, _g;
        const displayMessageId = `display-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        messageJsonStore[displayMessageId] = event;
        const validationErrors = event.validation_errors || [];
        if (event.error) {
            const messageHtml = `<span class="kind-chip kind-chip-error">error</span> Error: ${DOMPurify.sanitize(event.error)}`;
            appendMessage('agent error', messageHtml, displayMessageId, true, validationErrors);
            return;
        }
        if (event.contextId)
            contextId = event.contextId;
        switch (event.kind) {
            case 'task':
                if (event.status) {
                    const messageHtml = `<span class="kind-chip kind-chip-task">${event.kind}</span> Task created with status: ${DOMPurify.sanitize(event.status.state)}`;
                    appendMessage('agent progress', messageHtml, displayMessageId, true, validationErrors);
                }
                break;
            case 'status-update': {
                const statusText = (_d = (_c = (_b = (_a = event.status) === null || _a === void 0 ? void 0 : _a.message) === null || _b === void 0 ? void 0 : _b.parts) === null || _c === void 0 ? void 0 : _c[0]) === null || _d === void 0 ? void 0 : _d.text;
                if (statusText) {
                    const renderedContent = DOMPurify.sanitize(marked.parse(statusText));
                    const messageHtml = `<span class="kind-chip kind-chip-status-update">${event.kind}</span> Server responded with: ${renderedContent}`;
                    appendMessage('agent progress', messageHtml, displayMessageId, true, validationErrors);
                }
                break;
            }
            case 'artifact-update':
                (_f = (_e = event.artifact) === null || _e === void 0 ? void 0 : _e.parts) === null || _f === void 0 ? void 0 : _f.forEach(p => {
                    let content = null;
                    if ('text' in p && p.text) {
                        content = DOMPurify.sanitize(marked.parse(p.text));
                    }
                    else if ('file' in p && p.file) {
                        const { uri, mimeType } = p.file;
                        const sanitizedMimeType = DOMPurify.sanitize(mimeType);
                        const sanitizedUri = DOMPurify.sanitize(uri);
                        content = `File received (${sanitizedMimeType}): <a href="${sanitizedUri}" target="_blank" rel="noopener noreferrer">Open Link</a>`;
                    }
                    else if ('data' in p && p.data) {
                        content = `<pre><code>${DOMPurify.sanitize(JSON.stringify(p.data, null, 2))}</code></pre>`;
                    }
                    if (content !== null) {
                        const kindChip = `<span class="kind-chip kind-chip-artifact-update">${event.kind}</span>`;
                        const messageHtml = `${kindChip} ${content}`;
                        appendMessage('agent', messageHtml, displayMessageId, true, validationErrors);
                    }
                });
                break;
            case 'message': {
                const textPart = (_g = event.parts) === null || _g === void 0 ? void 0 : _g.find(p => p.text);
                if (textPart && textPart.text) {
                    const renderedContent = DOMPurify.sanitize(marked.parse(textPart.text));
                    const messageHtml = `<span class="kind-chip kind-chip-message">${event.kind}</span> ${renderedContent}`;
                    appendMessage('agent', messageHtml, displayMessageId, true, validationErrors);
                }
                break;
            }
        }
    });
    socket.on('debug_log', (log) => {
        const logEntry = document.createElement('div');
        const timestamp = new Date().toLocaleTimeString();
        let jsonString = JSON.stringify(log.data, null, 2);
        jsonString = jsonString.replace(/"method": "([^"]+)"/g, '<span class="json-highlight">"method": "$1"</span>');
        logEntry.className = `log-entry log-${log.type}`;
        logEntry.innerHTML = `
            <div>
                <span class="log-timestamp">${timestamp}</span>
                <strong>${log.type.toUpperCase()}</strong>
            </div>
            <pre>${jsonString}</pre>
        `;
        debugContent.appendChild(logEntry);
        if (!rawLogStore[log.id]) {
            rawLogStore[log.id] = {};
        }
        rawLogStore[log.id][log.type] = log.data;
        debugContent.scrollTop = debugContent.scrollHeight;
    });
    function appendMessage(sender, content, messageId, isHtml = false, validationErrors = []) {
        const placeholder = chatMessages.querySelector('.placeholder-text');
        if (placeholder)
            placeholder.remove();
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender.replace(' ', '-')}`;
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        if (isHtml) {
            messageContent.innerHTML = content;
        }
        else {
            messageContent.textContent = content;
        }
        messageElement.appendChild(messageContent);
        const statusIndicator = document.createElement('span');
        statusIndicator.className = 'validation-status';
        if (sender !== 'user') {
            if (validationErrors.length > 0) {
                statusIndicator.classList.add('invalid');
                statusIndicator.textContent = '⚠️';
                statusIndicator.title = validationErrors.join('\n');
            }
            else {
                statusIndicator.classList.add('valid');
                statusIndicator.textContent = '✅';
                statusIndicator.title = 'Message is compliant';
            }
            messageElement.appendChild(statusIndicator);
        }
        messageElement.addEventListener('click', (e) => {
            var _a;
            const target = e.target;
            if (target.tagName !== 'A') {
                const jsonData = sender === 'user'
                    ? (_a = rawLogStore[messageId]) === null || _a === void 0 ? void 0 : _a.request
                    : messageJsonStore[messageId];
                showJsonInModal(jsonData);
            }
        });
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
//# sourceMappingURL=script.js.map