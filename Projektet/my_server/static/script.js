//input type "hidden" är viktigt för upgiften, exempel value={{post[0]}}, id="post-id"

let person = {
    name: "",
    password: "",
};

const loadNewUserError = () => {
    console.log("Loading error message")
    let data_to_present = "Name and password already exists"
    document.getElementById("data_to_present").innerHTML = data_to_present;
}

const loadLoginUserError = () => {
    console.log("Loading error message")
    let data_to_present = "Incorrect name or password, please try again or create a new user"
    document.getElementById("data_to_present").innerHTML = data_to_present;
}

const loadForm = () => {
    console.log("Loading form")
    document.getElementById("theForm").submit()
}

$(document).ready(() => {

    $("#btnNewUser").click(() => {
        console.log("Creating new user");
        let name = document.getElementById("input_name").value;
        let password = document.getElementById("input_password").value;

        person.name = name;
        person.password = password;

        $.ajax({
            type: "POST",
            url: "/user/exist",
            data: JSON.stringify(person),
            dataType: "json",
            headers: {
                'Content-Type': 'application/json'
            }, 
            success: (response) => {
                if (response.success){
                    //gets response from python, response objet . msg runs this code if true
                    console.log(response.msg)
                    loadForm();
                }else{
                    console.log("Load Error")
                    console.log(response.msg)
                    loadNewUserError();
                }
            }
        });
    })

    $("#btnLoginUser").click(() => {
        console.log("Trying to login in user");
        let name = document.getElementById("input_name").value;
        let password = document.getElementById("input_password").value;

        person.name = name;
        person.password = password;

        $.ajax({
            type: "POST",
            url: "/user/exist",
            data: JSON.stringify(person),
            dataType: "json",
            headers: {
                'Content-Type': 'application/json'
            }, 
            success: (response) => {
                if (response.success){
                    //gets response from python, response objet . msg runs this code if true
                    console.log(response.msg)
                    loadLoginUserError();
                }else{
                    console.log("LoadForm")
                    console.log(response.msg)
                    loadForm();

                }
            }
        });
    })

})