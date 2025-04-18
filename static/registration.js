document.querySelector("form").addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const payload = {
      fullname: document.getElementById("fullname").value.trim(),
      email: document.getElementById("email").value.trim(),
      username: document.getElementById("username").value.trim(),
      password: document.getElementById("password").value.trim(),
      confirm_password: document.getElementById("confirm-password").value.trim(),
    };
  
    if (payload.password !== payload.confirm_password) {
      return alert("Passwords don’t match, bro.");
    }
  
    try {
      const res = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
  
      if (res.status === 200) {
        window.location.href = "/dashboard";
      } else {
        const err = await res.json();
        alert(err.message || "Registration failed.");
      }
    } catch (err) {
      alert("Shit broke. Try later.");
    }
  });
  