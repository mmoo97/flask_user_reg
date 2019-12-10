function displayloading() {
            document.getElementById("notification_window").innerHTML = "" +
                "<div class=\"joyride-tip-guide\" data-index=\"0\" style=\"visibility: visible; display: block; top: 77.5px; left: 570px;\"><span class=\"joyride-nub\" style=\"display: none;\"></span><div class=\"joyride-content-wrapper\" role=\"dialog\"><ol>\n" +
                "        <h4>\n" +
                "\n" +
                "          Your account is pending creation...\n" +
                "\n" +
                "        </h4>\n" +
                "                <br><p>\n" +
                "                    This can take between 5-10 min.\n" +
                "                </p>\n" +
                "      </ol>\n" +
                "                <img src=\"/static/img/loading.gif\" style=\"width: 35px; height: auto\"> Pending...\n" +
                "            </div></div>\n" +
                "\n" +
                "    <div class=\"joyride-modal-bg\" style=\"display: block;\"></div>"
}

function socketIO() {
    socket.emit('user data', {
        fullname: document.getElementById("fullname").value,
        reason: document.getElementById("reason").value,
        username: document.getElementById("username").innerText
    })
}