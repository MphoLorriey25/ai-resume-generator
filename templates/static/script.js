document.getElementById("generate-btn").addEventListener("click", async () => {
  const careerInfo = document.getElementById("career-info").value.trim();
  const template = document.getElementById("template").value;

  if (!careerInfo) {
    alert("Please enter your career info!");
    return;
  }

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ careerInfo, template }),
    });

    const data = await response.json();

    if (data.resume_text) {
      document.getElementById("resume-preview").innerText = data.resume_text;
    } else {
      alert("Failed to generate resume.");
    }
  } catch (error) {
    alert("Error generating resume.");
    console.error(error);
  }
});

async function exportResume(format) {
  const template = document.getElementById("template").value;
  const content = document.getElementById("resume-preview").innerText.trim();

  if (!content) {
    alert("Please generate the resume first.");
    return;
  }

  try {
    const response = await fetch("/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content, format, template }),
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume.${format === "pdf" ? "pdf" : "docx"}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } else {
      alert("Export failed");
    }
  } catch (error) {
    alert("Error exporting resume.");
    console.error(error);
  }
}

document.getElementById("export-pdf").addEventListener("click", () => exportResume("pdf"));
document.getElementById("export-word").addEventListener("click", () => exportResume("word"));
