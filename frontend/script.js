document.addEventListener('DOMContentLoaded', () => {
    const fileUpload = document.getElementById('file-upload');
    const fileName = document.getElementById('file-name');
    const analyzeBtn = document.getElementById('analyze-btn');
    const textInput = document.getElementById('text-input');
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');
    const downloadTxtBtn = document.getElementById('download-txt');
    const downloadDocxBtn = document.getElementById('download-docx');

    let currentCacheId = null;

    fileUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileName.textContent = e.target.files[0].name;
            fileName.style.color = 'var(--text)';
        } else {
            fileName.textContent = "No file selected";
            fileName.style.color = 'var(--text-light)';
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        const file = fileUpload.files[0];

        if (!text && !file) {
            alert('Please provide text or upload a file.');
            return;
        }

        const formData = new FormData();
        if (text) formData.append('text', text);
        if (file) formData.append('file', file);

        const originalBtnText = analyzeBtn.textContent;
        analyzeBtn.textContent = 'Processing Linguistically...';
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('http://127.0.0.1:8000/api/profile', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.status === 'success') {
                const s = data.stats;
                currentCacheId = data.cache_id;

                resultsSection.classList.remove('hidden');

                let complexityColor = '#10b981'; // Green for Low
                if (s.overall_complexity === 'Moderate Complexity') complexityColor = '#f59e0b'; // Yellow
                if (s.overall_complexity === 'High Complexity') complexityColor = '#ef4444'; // Red

                resultsContent.innerHTML = `
                    <div style="font-size: 1.2rem; margin-bottom: 1.5rem; text-align: center; background: white; padding: 1rem; border-radius: 8px; border-left: 5px solid ${complexityColor}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <strong>Overall System Classification:</strong> 
                        <span style="color: ${complexityColor}; font-weight: bold; font-size: 1.3rem; margin-left: 0.5rem">${s.overall_complexity}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
                        <div style="background: white; padding: 1.25rem; border-radius: 8px; border: 1px solid var(--border);">
                            <h3 style="margin-top: 0; font-size: 1rem; color: var(--primary); border-bottom: 2px solid var(--bg); padding-bottom: 0.5rem">1. Sentence Length</h3>
                            <div style="margin-bottom: 0.25rem;">Total Words: <strong>${s.length_stats.total_words}</strong></div>
                            <div style="margin-bottom: 0.25rem;">Total Sentences: <strong>${s.length_stats.total_sentences}</strong></div>
                            <div>Avg Length: <strong>${s.length_stats.avg_length}</strong></div>
                        </div>
                        <div style="background: white; padding: 1.25rem; border-radius: 8px; border: 1px solid var(--border);">
                            <h3 style="margin-top: 0; font-size: 1rem; color: var(--primary); border-bottom: 2px solid var(--bg); padding-bottom: 0.5rem">2. Grammatical Structure</h3>
                            <div style="margin-bottom: 0.25rem;">Total Clauses: <strong>${s.grammar_stats.total_clauses}</strong></div>
                            <div>Subordinate Clauses: <strong>${s.grammar_stats.subordinate_clauses}</strong></div>
                        </div>
                        <div style="background: white; padding: 1.25rem; border-radius: 8px; border: 1px solid var(--border);">
                            <h3 style="margin-top: 0; font-size: 1rem; color: var(--primary); border-bottom: 2px solid var(--bg); padding-bottom: 0.5rem">3. Noun Phrases (NPs)</h3>
                            <div style="margin-bottom: 0.25rem;">Total NPs: <strong>${s.np_stats.total_nps}</strong></div>
                            <div style="margin-bottom: 0.25rem;">Avg NP Length: <strong>${s.np_stats.avg_np_length}</strong></div>
                            <div>Modifiers: <strong>${s.np_stats.total_modifiers}</strong></div>
                        </div>
                        <div style="background: white; padding: 1.25rem; border-radius: 8px; border: 1px solid var(--border);">
                            <h3 style="margin-top: 0; font-size: 1rem; color: var(--primary); border-bottom: 2px solid var(--bg); padding-bottom: 0.5rem">4. Linguistic Features</h3>
                            <div style="margin-bottom: 0.25rem;">Unique Words: <strong>${s.feature_stats.unique_words}</strong></div>
                            <div>Lexical Diversity (0-1): <strong>${s.feature_stats.lexical_diversity}</strong></div>
                        </div>
                    </div>
                `;

                downloadTxtBtn.disabled = false;
                downloadDocxBtn.disabled = false;

                resultsSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Analysis Error: ' + data.message);
            }
        } catch (error) {
            alert('Error connecting to backend API. Ensure the fastAPI server is running locally.');
            console.error(error);
        } finally {
            analyzeBtn.textContent = originalBtnText;
            analyzeBtn.disabled = false;
        }
    });

    downloadTxtBtn.addEventListener('click', () => {
        if (currentCacheId) {
            window.location.href = `http://127.0.0.1:8000/api/download/txt/${currentCacheId}`;
        }
    });

    downloadDocxBtn.addEventListener('click', () => {
        if (currentCacheId) {
            window.location.href = `http://127.0.0.1:8000/api/download/docx/${currentCacheId}`;
        }
    });
});
