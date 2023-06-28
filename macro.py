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
    
checkVideo = """
    function timeToSeconds(timeString) {
        var parts = timeString.split(":");
        return parseInt(parts[0]) * 60 + parseInt(parts[1]);
    }
    
    var percents = document.querySelectorAll("#per_text");
    for (let i = 0; i < percents.length; i++) {
        if (percents[i].textContent.includes("100%")) continue;
        
        var target = percents[i].parentNode.parentNode;
        var timeString = target.children[1].children[2].textContent;
        var times = timeString.split(" / ");
        var currentTime = timeToSeconds(times[0]);
        var totalTime = timeToSeconds(times[1]);
        var timeArray = {
            currentTime: currentTime,
            totalTime: totalTime,
        };
        
        localStorage.setItem("timeArray", JSON.stringify(timeArray));
        target.querySelector(".site-mouseover-color").click();
        break;
    }
    location.href = "https://eclass.seoultech.ac.kr/ilos/main/main_form.acl";
"""

watchingVideo = """
    var timeArray = localStorage.getItem("timeArray");
    timeArray = JSON.parse(timeArray);
    setTimeout(() => window.history.back(), timeArray["remainingTime"] * 1000 + 300);

    function sleep(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

    async function showProgress(timeArray) {
        const updateInterval = 5000;
        const iterations = timeArray["totalTime"] + 300;

        for (let i = timeArray["currentTime"]; i <= iterations; i += 5) {
            let percentage = Math.floor((i / iterations) * 100);
            console.log(`Progress: ${percentage}%\r`);
            await sleep(updateInterval);
        }
        console.log("Complete: 100%\r");
    }

    showProgress(timeArray);
"""