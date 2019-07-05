
function login()
{
    document.getElementById('pop_inq').style.display = "none";
    document.getElementById('pop_reg').style.display = "none";
    document.getElementById('pop_login').style.display = "block";
}
function reg()
{
    document.getElementById('pop_inq').style.display = "none";
    document.getElementById('pop_login').style.display = "none";
    document.getElementById('pop_reg').style.display = "block";
}
function inq()
{
    document.getElementById('pop_inq').style.display = "block";
    document.getElementById('pop_login').style.display = "none";
    document.getElementById('pop_reg').style.display = "none";
 }
function clos()
{
    document.getElementById('pop_login').style.display = "none";
    document.getElementById('pop_reg').style.display = "none";
    document.getElementById('pop_inq').style.display = "none";
}
function reg_from_sub()
{
    var pass = document.reg_form.reg_pwd.value;
    var repass = document.reg_form.reg_repwd.value;
    if(pass.length < 6)
    {
        document.getElementById('reg_p_pwd').innerHTML = "Password must be at least 6 Characters.";
        document.getElementById('reg_p_pwd').style.display = "block";
        document.getElementById('reg_p_repwd').style.display = "none";
        return false;
    }
    else if(pass != repass)
    {
        document.getElementById('reg_p_repwd').innerHTML = "Password must be Similer.";
        document.getElementById('reg_p_repwd').style.display = "block";
        document.getElementById('reg_p_pwd').style.display = "none";
        return false;
    }
}