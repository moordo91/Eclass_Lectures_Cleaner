startAndCheckClass = """
        popTodo();
        var elements = document.getElementsByClassName("todo_title");
        for (let i = 0; i < elements.length; i++) {
            if (elements[i].textContent.includes("[온라인강의]")) {
            elements[i].parentNode.click();
            break;
            }
        }
        alert("모든 강의를 수강하셨습니다!");
    """