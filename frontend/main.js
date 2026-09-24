import { createIcons } from 'lucide';
import { marked } from 'marked';

// Initialize Icons
createIcons();

// Use VITE_API_URL if deployed, otherwise fallback to localhost
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// State
let projectName = '';

// DOM Elements
const btnInit = document.getElementById('btnInit');
const btnExpand = document.getElementById('btnExpand');
const btnIngest = document.getElementById('btnIngest');
const btnHumanize = document.getElementById('btnHumanize');

const step1 = document.getElementById('step-1');
const step2 = document.getElementById('step-2');
const step3 = document.getElementById('step-3');
const step4 = document.getElementById('step-4');

const moveToStep = (current, next) => {
  current.classList.remove('active');
  setTimeout(() => {
    next.classList.add('active');
  }, 500);
};

// Step 1: Initialize
btnInit.addEventListener('click', async () => {
  const nameInput = document.getElementById('projectName').value.trim();
  const errorText = document.getElementById('initError');
  
  if (!nameInput) {
    errorText.textContent = "Please enter a project name.";
    return;
  }
  
  btnInit.innerHTML = '<div class="loader" style="width:20px;height:20px;border-width:2px;margin:0;"></div>';
  
  try {
    const res = await fetch(`${API_BASE}/project`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_name: nameInput })
    });
    
    if (res.ok) {
      projectName = nameInput;
      moveToStep(step1, step2);
    } else {
      const data = await res.json();
      errorText.textContent = data.detail || "Failed to initialize project.";
    }
  } catch (err) {
    errorText.textContent = "Cannot connect to backend server.";
  } finally {
    btnInit.innerHTML = 'Initialize Project <i data-lucide="arrow-right"></i>';
    createIcons();
  }
});

// Step 2: Expand Idea
btnExpand.addEventListener('click', async () => {
  const idea = document.getElementById('userIdea').value.trim();
  if (!idea) return;
  
  const loader = document.getElementById('loaderExpand');
  const resultBox = document.getElementById('outlineResult');
  const btnNext = document.getElementById('btnNextToIngest');
  
  btnExpand.style.display = 'none';
  loader.style.display = 'inline-block';
  resultBox.style.display = 'none';
  
  try {
    const res = await fetch(`${API_BASE}/expand`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_name: projectName, idea })
    });
    
    const data = await res.json();
    if (res.ok) {
      resultBox.innerHTML = marked.parse(data.outline);
      resultBox.style.display = 'block';
      loader.style.display = 'none';
      btnNext.style.display = 'inline-flex';
    } else {
      alert("Error: " + data.detail);
      btnExpand.style.display = 'inline-flex';
      loader.style.display = 'none';
    }
  } catch (err) {
    alert("Connection error.");
    btnExpand.style.display = 'inline-flex';
    loader.style.display = 'none';
  }
});

document.getElementById('btnNextToIngest').addEventListener('click', () => {
  moveToStep(step2, step3);
});

// Step 3: Ingest PDF
btnIngest.addEventListener('click', async () => {
  const fileInput = document.getElementById('pdfUpload');
  if (!fileInput.files.length) {
    alert("Please select a PDF file first.");
    return;
  }
  
  const loader = document.getElementById('loaderIngest');
  const resultBox = document.getElementById('graphResult');
  const btnNext = document.getElementById('btnNextToHumanize');
  
  btnIngest.style.display = 'none';
  loader.style.display = 'inline-block';
  
  const formData = new FormData();
  formData.append("project_name", projectName);
  formData.append("file", fileInput.files[0]);
  
  try {
    const res = await fetch(`${API_BASE}/ingest`, {
      method: 'POST',
      body: formData
    });
    
    const data = await res.json();
    if (res.ok) {
      resultBox.innerHTML = `<h3>Knowledge Graph Built Successfully!</h3><pre style="white-space:pre-wrap;font-size:0.8rem;">${data.graph_summary}</pre>`;
      resultBox.style.display = 'block';
      loader.style.display = 'none';
      btnNext.style.display = 'inline-flex';
    } else {
      alert("Error: " + data.detail);
      btnIngest.style.display = 'inline-flex';
      loader.style.display = 'none';
    }
  } catch (err) {
    alert("Connection error.");
    btnIngest.style.display = 'inline-flex';
    loader.style.display = 'none';
  }
});

document.getElementById('btnNextToHumanize').addEventListener('click', () => {
  moveToStep(step3, step4);
});

// Step 4: Humanize
btnHumanize.addEventListener('click', async () => {
  const loader = document.getElementById('loaderHumanize');
  const resultBox = document.getElementById('litReviewResult');
  const exportText = document.getElementById('exportPath');
  
  btnHumanize.style.display = 'none';
  loader.style.display = 'inline-block';
  
  try {
    const res = await fetch(`${API_BASE}/humanize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_name: projectName })
    });
    
    const data = await res.json();
    if (res.ok) {
      resultBox.innerHTML = marked.parse(data.lit_review);
      resultBox.style.display = 'block';
      exportText.textContent = `🎉 Project exported successfully to: ${data.export_path}`;
      loader.style.display = 'none';
    } else {
      alert("Error: " + data.detail);
      btnHumanize.style.display = 'inline-flex';
      loader.style.display = 'none';
    }
  } catch (err) {
    alert("Connection error.");
    btnHumanize.style.display = 'inline-flex';
    loader.style.display = 'none';
  }
});

// File upload UX
const fileInput = document.getElementById('pdfUpload');
const fileBox = document.querySelector('.file-upload-box span');
fileInput.addEventListener('change', (e) => {
  if (e.target.files.length) {
    fileBox.textContent = e.target.files[0].name;
  }
});
