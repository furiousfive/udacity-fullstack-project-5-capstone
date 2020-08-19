// logout
const logOut = () => {
  localStorage.clear()
  window.location.href = 'https://jamaalsanders.auth0.com/v2/logout'
};