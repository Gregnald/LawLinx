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

  alert("No API endpoint for registration yet. Ask dev to implement it at /api/register.");
});
