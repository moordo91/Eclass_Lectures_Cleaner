popTodo();

var target;
var elements = document.getElementsByClassName('todo_title');
for (let i = 0; i < elements.length; i++) {
    if (elements[i].textContent.includes("[온라인강의]")) {
        target = elements[i];
        elements[i].parentNode.click();
        break;
    }
}

var percents = document.getElementById('per_text')
for (let i = 0; i < percents.length; i++) {
    if (percents[i].textContent.includes("100%"))
        continue;
    
}