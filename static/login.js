document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  try {
    const res = await fetch(`https://1f42-115-241-34-101.ngrok-free.app/api/users/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
      method: "POST",
      mode: "cors"
    });

    const contentType = res.headers.get("content-type");

    if (!res.ok) {
      const errText = await res.text();
      return alert(`❌ Server error: ${res.status}\n\n${errText}`);
    }

    if (contentType && contentType.includes("application/json")) {
      const data = await res.json();
      if (data.message === "login successful") {
        alert("✅ Login successful!");
        window.location.href = "/dashboard";
      } else {
        alert("❌ " + (data.message || "Invalid credentials"));
      }
    } else {
      const raw = await res.text();
      alert("⚠️ Unexpected response:\n\n" + raw);
    }

  } catch (err) {
    alert("🚫 Network error: " + err.message);
  }
});
