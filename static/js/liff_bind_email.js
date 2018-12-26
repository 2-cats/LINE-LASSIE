window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    liff.getProfile().then(
            profile=>{
                console.log(profile)
                document.getElementById("userName").innerHTML = "『" + profile.displayName + " ，您好！我是 Lassie！』";
            }
    ).catch(function (error) {
        window.alert("Error getting profile: " + error);
    });
}
