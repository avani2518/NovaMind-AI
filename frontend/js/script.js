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
        "40px";

    wrapper.style.marginBottom =
        "70px";

    wrapper.innerHTML =
        `
        <a
            href="/frontend/index.html"
            class="primary-btn"
            style="
                text-decoration:none;
                padding:18px 36px;
                border-radius:16px;
                font-size:17px;
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

    // =========================================
    // ADD BELOW DASHBOARD
    // =========================================

    const dashboard =
        document.querySelector(
            ".dashboard-section"
        );

    dashboard.insertAdjacentElement(
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
            generateDashboard(data.answer);

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

function generateDashboard(answer) {

    // WORD COUNT

    const words =
        answer.split(/\s+/).length;

    document.getElementById(
        "wordCount"
    ).innerText = words;


    // SENTENCE COUNT

    const sentences =
        answer.split(/[.!?]+/).length;

    document.getElementById(
        "sentenceCount"
    ).innerText = sentences;


    // READING TIME

    const readingTime =
        Math.ceil(words / 200);

    document.getElementById(
        "readingTime"
    ).innerText =
        `${readingTime} min`;


    // COMPLEXITY SCORE

    const complexity =
        Math.min(
            95,
            Math.floor(words / 12)
        );

    document.getElementById(
        "complexityScore"
    ).innerText =
        `${complexity}%`;


    // KEYWORDS

    const keywordContainer =
        document.getElementById(
            "keywordContainer"
        );

    keywordContainer.innerHTML = "";

    const commonWords = [
        "the","and","is","to","of",
        "in","for","a","on","with",
        "that","this","as","are"
    ];

    const wordFrequency = {};

    answer
        .toLowerCase()
        .split(/\W+/)
        .forEach(word => {

            if (
                word.length > 4 &&
                !commonWords.includes(word)
            ) {

                wordFrequency[word] =
                    (wordFrequency[word] || 0) + 1;
            }
        });

    const keywords =
        Object.entries(wordFrequency)
            .sort((a,b)=>b[1]-a[1])
            .slice(0,10);

    keywords.forEach(keyword => {

        const tag =
            document.createElement("div");

        tag.className =
            "keyword-tag";

        tag.innerText =
            keyword[0];

        keywordContainer.appendChild(tag);
    });


    // CHART

    const ctx =
        document.getElementById(
            "topicChart"
        );

    new Chart(ctx, {

        type:"doughnut",

        data:{

            labels:[
                "Research",
                "Methodology",
                "Results",
                "Analysis",
                "Concepts"
            ],

            datasets:[{

                data:[
                    25,
                    20,
                    18,
                    22,
                    15
                ]
            }]
        },

        options:{

            responsive:true,

            plugins:{

                legend:{
                    position:"bottom"
                }
            }
        }
    });
}