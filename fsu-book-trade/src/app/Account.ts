export class Account
{
    avatar:string;
    email:string;
    firstname:string;
    fsuid:string;
    lastname:string;
    num_of_posts:number;
    password:string;
    username:string;


    constructor(avatar, email, firstname, fsuid, lastname, num_of_posts, password, username)
    {
        this.avatar = avatar;
        this.email = email;
        this.firstname = firstname;
        this.fsuid = fsuid;
        this.lastname = lastname;
        this.num_of_posts = num_of_posts;
        this.password = password;
        this.username = username;
    }

}