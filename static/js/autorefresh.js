let autorefreshEnabled = false;
function toggleAutorefresh() {
    autorefreshEnabled = !autorefreshEnabled;
    if (autorefreshEnabled) {
      localStorage.setItem("autorefreshEnabled", "true");
    } else {
        localStorage.removeItem("autorefreshEnabled");
    }
}

let storedAutorefreshEnabled = localStorage.getItem("autorefreshEnabled");
if (storedAutorefreshEnabled === "true") {
    autorefreshEnabled = true;
}

setInterval(function() {
    if (autorefreshEnabled) {
      location.reload();
    }
}, 400);