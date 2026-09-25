* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6fb;
    color: #222;
}

.container {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
}

.header {
    text-align: center;
    background: white;
    padding: 30px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.header h1 {
    font-size: 36px;
    margin-bottom: 10px;
}

.header p {
    color: #666;
}

.controls {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.controls label {
    display: block;
    margin-top: 12px;
    margin-bottom: 5px;
    font-weight: bold;
}

.controls select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
}

.primary-btn {
    margin-top: 20px;
    padding: 12px 25px;
    border: none;
    border-radius: 8px;
    background: #4f46e5;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

.primary-btn:hover {
    opacity: 0.85;
}

.question-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.question-number {
    color: #4f46e5;
    font-weight: bold;
    margin-bottom: 10px;
}

.question-text {
    font-size: 20px;
    font-weight: bold;
}

.options {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.option-btn {
    padding: 12px;
    border: 1px solid #ccc;
    background: white;
    border-radius: 8px;
    text-align: left;
    cursor: pointer;
    font-size: 16px;
}

.option-btn:hover {
    background: #f0f0ff;
}

.option-btn:disabled {
    cursor: not-allowed;
}

.correct-answer {
    background: #d1fae5 !important;
    border-color: #10b981 !important;
}

.wrong-answer {
    background: #fee2e2 !important;
    border-color: #ef4444 !important;
}

.result {
    font-weight: bold;
    margin-top: 15px;
}

.correct {
    color: #059669;
}

.wrong {
    color: #dc2626;
}
.danger-zone {
    margin-top: 30px;
    padding: 24px;
    border: 1px solid #ef4444;
    border-radius: 16px;
    background: #fff5f5;
}

.danger-zone h3 {
    color: #dc2626;
    margin-bottom: 8px;
}

.danger-zone p {
    color: #666;
    margin-bottom: 16px;
}

.delete-all-btn {
    background: #dc2626;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
}

.delete-all-btn:hover {
    background: #b91c1c;
}