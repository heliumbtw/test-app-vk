function searchFunction() {

  const input = document
    .getElementById('searchInput')
    .value.trim().toUpperCase();

  const friendsList = document
    .getElementById("myUL")
    .getElementsByTagName('li');

  Array.from(friendsList)
    .map(elem => elem.getElementsByTagName("a")[0])
    .map(elem => elem.textContent || elem.innerText)
    .map(name => name.toUpperCase())
    .map(name => name.indexOf(input) > -1)
    .forEach((containsInput, index) =>
      friendsList[index].style.display = containsInput ? '' : 'none'
    );
}
document.getElementById('searchInput').addEventListener('onkeyup', searchFunction);