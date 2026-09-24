const fs = require('fs');

let content = fs.readFileSync('hr-helper/index.html', 'utf8');

const target = `        async function downloadShortlistedZIP() {
            const shortlisted = bulkResults.filter(r => r.status === 'shortlisted');
            if (!shortlisted.length) {
                alert('No candidates shortlisted yet! Click ⭐ on candidates to shortlist them first.');
                return;
            }
            if (!window.JSZip) {
                alert('ZIP generator module is loading...');
                return;
            }`;

const replacement = `        async function downloadShortlistedZIP() {
            const shortlisted = bulkResults.filter(r => r.status === 'shortlisted');
            if (!shortlisted.length) {
                alert('No candidates shortlisted yet! Click ⭐ on candidates to shortlist them first.');
                return;
            }
            await loadHrLibraries();
            if (!window.JSZip) {
                alert('ZIP generator module is loading... Please try again.');
                return;
            }`;

// Normalize newlines for replacement
const normalizedContent = content.replace(/\r\n/g, '\n');
const normalizedTarget = target.replace(/\r\n/g, '\n');
const normalizedReplacement = replacement.replace(/\r\n/g, '\n');

if (normalizedContent.includes(normalizedTarget)) {
    const updated = normalizedContent.replace(normalizedTarget, normalizedReplacement);
    // write back with original line endings if needed or standard
    fs.writeFileSync('hr-helper/index.html', updated, 'utf8');
    console.log('Successfully patched hr-helper/index.html');
} else {
    console.error('Target not found!');
}
