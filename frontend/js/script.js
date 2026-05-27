const API_KEY = "avani123";


// =========================================
// PDF FILE INPUT
// =========================================

const pdfInput =
    document.getElementById("pdfFile");


if (pdfInput) {

    pdfInput.addEventListener(
        "change",
        () => {

            const file =
                pdfInput.files[0];

            document.getElementById(
                "fileName"
            ).innerHTML =
                file
                ? `📄 Selected File: ${file.name}`
                : "";
        }
    );
}


// =========================================
// PDF UPLOAD
// =========================================

const uploadForm =
    document.getElementById(
        "uploadForm"
    );


if (uploadForm) {

    uploadForm.addEventListener(
        "submit",
        async (e) => {

            e.preventDefault();

            const file =
                pdfInput.files[0];

            const status =
                document.getElementById(
                    "uploadStatus"
                );

            if (!file) {

                status.innerHTML =
                    `
                    <div class="answer-placeholder">
                        ❌ Please select a PDF file
                    </div>
                    `;

                return;
            }

            status.innerHTML =
                `
                <div class="loading-container">

                    <div class="loader"></div>

                    <p>
                        Uploading and processing PDF...
                    </p>

                </div>
                `;

            const formData =
                new FormData();

            formData.append(
                "file",
                file
            );

            try {

                const response =
                    await fetch(
                        "http://127.0.0.1:8000/ingest/pdf",
                        {
                            method:"POST",

                            headers:{
                                "X-API-Key":API_KEY
                            },

                            body:formData
                        }
                    );

                const data =
                    await response.json();

                if (response.ok) {

                    status.innerHTML =
                        `
                        <div class="ai-answer">

                            <div class="ai-badge">
                                Upload Successful
                            </div>

                            <div class="answer-content">

                                ✅ Your PDF has been processed successfully.

                                <br><br>

                                Redirecting to NovaMind AI...

                            </div>

                        </div>
                        `;

                    setTimeout(() => {

                        window.location.href =
                            "/frontend/result.html";

                    }, 1800);

                } else {

                    status.innerHTML =
                        `
                        <div class="answer-placeholder">
                            ❌ ${data.detail}
                        </div>
                        `;
                }

            } catch (error) {

                console.error(error);

                status.innerHTML =
                    `
                    <div class="answer-placeholder">
                        ❌ Server connection failed
                    </div>
                    `;
            }
        }
    );
}


// =========================================
// ASK AI
// =========================================

const askBtn =
    document.getElementById("askBtn");


const questionInput =
    document.getElementById(
        "questionInput"
    );


// =========================================
// ENTER KEY SUPPORT
// =========================================

if (questionInput) {

    questionInput.addEventListener(
        "keypress",
        function(event) {

            if (event.key === "Enter") {

                event.preventDefault();

                if (askBtn) {

                    askBtn.click();
                }
            }
        }
    );
}


// =========================================
// FORMAT AI RESPONSE
// =========================================

function formatAnswer(answer) {

    let formattedAnswer = answer;

    formattedAnswer = formattedAnswer

        // Headings
        .replace(/### (.*?)(\n|$)/g, "<h3>$1</h3>")

        .replace(/## (.*?)(\n|$)/g, "<h2>$1</h2>")

        // Bold text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")

        // Bullet points
        .replace(/\n- /g, "<br>• ")

        // Numbered lists
        .replace(/\n\d+\.\s/g, "<br><br>• ")

        // Remove large gaps
        .replace(/\n{3,}/g, "\n\n")

        // Normal line breaks
        .replace(/\n\n/g, "<br><br>")
        .replace(/\n/g, "<br>");

    return formattedAnswer;
}


// =========================================
// CREATE BACK BUTTON
// =========================================

function createBackButton() {

    const existingButton =
        document.getElementById(
            "backHomeWrapper"
        );

    if (existingButton) {

        existingButton.remove();
    }

    const wrapper =
        document.createElement("div");

    wrapper.id =
        "backHomeWrapper";

    wrapper.style.width =
        "100%";

    wrapper.style.display =
        "flex";

    wrapper.style.justifyContent =
        "center";

    wrapper.style.alignItems =
        "center";

    wrapper.style.marginTop =
        "30px";

    wrapper.style.marginBottom =
        "60px";

    wrapper.innerHTML =
        `
        <a
            href="/frontend/index.html"
            class="primary-btn"
            style="
                text-decoration:none;
                padding:16px 34px;
                border-radius:14px;
                font-size:16px;
                font-weight:600;
                display:inline-flex;
                align-items:center;
                justify-content:center;
                gap:10px;
            "
        >
            ← Back To Home
        </a>
        `;

    // ADD BUTTON BELOW RESPONSE BOX

    const answerBox =
        document.getElementById(
            "answerBox"
        );

    answerBox.insertAdjacentElement(
        "afterend",
        wrapper
    );
}


// =========================================
// ASK QUESTION FUNCTION
// =========================================

async function askQuestion() {

    const question =
        questionInput.value.trim();

    const answerBox =
        document.getElementById(
            "answerBox"
        );

    if (!question) {

        answerBox.innerHTML =
            `
            <div class="answer-placeholder">
                Please enter a question.
            </div>
            `;

        return;
    }

    answerBox.innerHTML =
        `
        <div class="loading-container">

            <div class="loader"></div>

            <p>
                NovaMind AI is analyzing your document...
            </p>

        </div>
        `;

    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/ask",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":"application/json",
                        "X-API-Key":API_KEY
                    },

                    body:JSON.stringify({
                        question:question
                    })
                }
            );

        const data =
            await response.json();

        if (response.ok) {

            let finalAnswer = "";

            if (typeof data.answer === "string") {

                finalAnswer =
                    formatAnswer(
                        data.answer
                    );

            } else {

                finalAnswer =
                    formatAnswer(
                        JSON.stringify(
                            data.answer,
                            null,
                            2
                        )
                    );
            }

            answerBox.innerHTML =
                `
                <div class="ai-answer">

                    <div class="ai-badge">
                        AI Response
                    </div>

                    <div class="answer-content">

                        ${finalAnswer}

                    </div>

                </div>
                `;

            createBackButton();

        } else {

            answerBox.innerHTML =
                `
                <div class="answer-placeholder">
                    ❌ ${data.detail}
                </div>
                `;
        }

    } catch (error) {

        console.error(error);

        answerBox.innerHTML =
            `
            <div class="answer-placeholder">
                ❌ Failed to connect to NovaMind server
            </div>
            `;
    }
}


// =========================================
// ASK BUTTON CLICK
// =========================================

if (askBtn) {

    askBtn.addEventListener(
        "click",
        askQuestion
    );
}

// =========================================
// LOAD AI DASHBOARD
// =========================================

async function loadSuggestions() {

    const container =
        document.getElementById(
            "suggestionsContainer"
        );

    if (!container) return;

    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/suggestions"
            );

        const data =
            await response.json();

        if (response.ok) {

            container.innerHTML = "";

            data.questions.forEach(
                (question) => {

                    const button =
                        document.createElement(
                            "button"
                        );

                    button.className =
                        "suggestion-btn";

                    button.innerText =
                        question;

                    button.addEventListener(
                        "click",
                        () => {

                            questionInput.value =
                                question;

                            askQuestion();
                        }
                    );

                    container.appendChild(
                        button
                    );
                }
            );
        }

    } catch (error) {

        console.error(error);
    }
}


loadSuggestions();