// function domainPage() {

//     document.getElementById("domain_inp1").hidden = true;
//     document.getElementById("domain_inp2").hidden = true;
// }

function validateFormreport() {

    var flag = true;

    var report = document.forms["reportgen"]["mailid"].value;
    console.log(report)
            if  (report){
                    // console.log("Inside")
                    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(report)) {
                        
                            document.getElementById("mail_id").hidden = true;

                        
                        } else {
                            console.log("else")
                            document.getElementById("mail_id").hidden = false;
                            flag = false;
                        }
                    }
    if (flag) {

        return true;

    } else {

        return false;
    }
    }
