document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
  
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
  
      const data = await res.json();
  
      if (data.message === "login successful") {
        window.location.href = "/dashboard";
      } else {
        alert("Invalid credentials. Try again.");
      }
    } catch (err) {
      alert("Server error. Chill and retry.");
    }
  });
  