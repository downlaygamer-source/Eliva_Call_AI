// Eliva Simulator Client-Side Logic (Voice + Text + Web Speech API)

let currentCallSid = null;
let isCallActive = false;
let recognition = null;
let isRecording = false;

// Initialize Web Speech API for Browser Voice Input (STT)
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("userInput").value = transcript;
        sendCallerMessage();
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error:", event.error);
        stopVoiceInput();
    };

    recognition.onend = function() {
        stopVoiceInput();
    };
}

// Text-to-Speech (TTS) using Browser SpeechSynthesis
function speakText(text) {
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel(); // Stop any previous speech
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 1.05;
        utterance.pitch = 1.1; // Friendly assistant voice

        // Find a pleasant female voice if available
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => (v.name.includes("Samantha") || v.name.includes("Zira") || v.name.includes("Google US English") || v.name.includes("Female") || v.name.includes("Natural")) && v.lang.startsWith("en"));
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        window.speechSynthesis.speak(utterance);
    }
}

// Start Call
async function startSimulatedCall() {
    const callerName = document.getElementById("callerName").value.trim() || "Caller";
    const callerPhone = document.getElementById("callerPhone").value.trim() || "+1-555-0100";

    try {
        const res = await fetch("/api/simulate/start", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ caller_name: callerName, caller_phone: callerPhone })
        });
        const data = await res.json();

        currentCallSid = data.call_sid;
        isCallActive = true;

        // Update UI
        document.getElementById("startCallBtn").disabled = true;
        document.getElementById("endCallBtn").disabled = false;
        document.getElementById("userInput").disabled = false;
        document.getElementById("sendBtn").disabled = false;
        if (recognition) document.getElementById("micBtn").disabled = false;

        const badge = document.getElementById("callStatusBadge");
        badge.className = "inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-xs text-emerald-300 font-medium self-start";
        badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span><span>Call Active (Eliva connected)</span>`;

        // Render Initial Greeting
        renderTranscript(data.transcript);
        document.getElementById("summaryCard").classList.add("hidden");

        // Speak Greeting
        speakText(data.greeting);

    } catch (err) {
        alert("Failed to start call: " + err);
    }
}

// Send Caller Speech/Message
async function sendCallerMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text || !isCallActive || !currentCallSid) return;

    input.value = "";
    document.getElementById("processingIndicator").classList.remove("hidden");

    // Add caller speech immediately to UI
    appendMessageToTranscript("Caller", text);

    try {
        const res = await fetch("/api/simulate/talk", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ call_sid: currentCallSid, speech: text })
        });
        const data = await res.json();

        document.getElementById("processingIndicator").classList.add("hidden");

        if (data.reply) {
            appendMessageToTranscript("Eliva", data.reply);
            speakText(data.reply);
        }

    } catch (err) {
        document.getElementById("processingIndicator").classList.add("hidden");
        appendMessageToTranscript("Eliva", "Sorry, I had a brief network glitch. Could you repeat that?");
    }
}

// End Call
async function endSimulatedCall() {
    if (!currentCallSid) return;

    window.speechSynthesis.cancel();
    stopVoiceInput();

    try {
        const res = await fetch("/api/simulate/end", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ call_sid: currentCallSid })
        });
        const data = await res.json();

        isCallActive = false;

        // Reset UI
        document.getElementById("startCallBtn").disabled = false;
        document.getElementById("endCallBtn").disabled = true;
        document.getElementById("userInput").disabled = true;
        document.getElementById("sendBtn").disabled = true;
        document.getElementById("micBtn").disabled = true;

        const badge = document.getElementById("callStatusBadge");
        badge.className = "inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-400 font-medium self-start";
        badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-slate-500"></span><span>Call Finished</span>`;

        // Render AI Summary Card
        if (data.summary && data.summary.extracted_info) {
            const info = data.summary.extracted_info;
            document.getElementById("summaryCard").classList.remove("hidden");
            document.getElementById("summaryBadge").textContent = info.category || "Call Completed";
            document.getElementById("summaryText").textContent = info.summary || "No summary generated.";

            const list = document.getElementById("actionItemsList");
            list.innerHTML = "";
            (info.action_items || ["No specific follow-up required"]).forEach(item => {
                const li = document.createElement("li");
                li.textContent = item;
                list.appendChild(li);
            });
        }

    } catch (err) {
        console.error(err);
    }
}

function handleKeyPress(e) {
    if (e.key === "Enter") {
        sendCallerMessage();
    }
}

function sendQuickPrompt(promptText) {
    if (!isCallActive) {
        alert("Please click 'Dial In' first to start the call session.");
        return;
    }
    document.getElementById("userInput").value = promptText;
    sendCallerMessage();
}

function toggleVoiceInput() {
    if (!recognition) {
        alert("Voice speech recognition is not supported in this browser. Please use Chrome/Edge or type your message.");
        return;
    }
    if (isRecording) {
        recognition.stop();
        stopVoiceInput();
    } else {
        recognition.start();
        isRecording = true;
        const micBtn = document.getElementById("micBtn");
        micBtn.classList.add("mic-active");
    }
}

function stopVoiceInput() {
    isRecording = false;
    const micBtn = document.getElementById("micBtn");
    if (micBtn) micBtn.classList.remove("mic-active");
}

function renderTranscript(transcript) {
    const box = document.getElementById("transcriptBox");
    box.innerHTML = "";
    transcript.forEach(t => appendMessageToTranscript(t.speaker, t.text));
}

function appendMessageToTranscript(speaker, text) {
    const box = document.getElementById("transcriptBox");
    const div = document.createElement("div");
    div.className = `flex flex-col ${speaker === 'Eliva' ? 'items-start' : 'items-end'} space-y-1 text-xs`;

    const isEliva = speaker === "Eliva";
    div.innerHTML = `
        <span class="text-[10px] font-semibold ${isEliva ? 'text-indigo-400' : 'text-emerald-400'}">${speaker}</span>
        <div class="p-3 rounded-2xl max-w-[85%] ${isEliva ? 'bg-slate-800/90 text-slate-100 rounded-tl-sm border border-slate-700/50' : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-tr-sm shadow-md'} leading-relaxed">
            ${text}
        </div>
    `;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
