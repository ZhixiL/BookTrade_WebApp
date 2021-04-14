export class Textbook
{
    author:string;
    bookname:string;
    by:string;
    college:string;
    description:string;
    id:number;
    picture:string;
    price:number;
    stat:string;
    time:string;


    constructor(author, bookname, by, college, description, id,
        picture, price, stat, time)
    {
        this.author = author;
        this.bookname = bookname;
        this.by = by;
        this.college = college;
        this.description = description;
        this.id = id;
        this.picture = picture;
        this.price = price;
        this.stat = stat;
        this.time = time;
    }

}

export class buyOrderPost
{
    author:string;
    bookname:string;
    by:string;
    college:string;
    id:number;
    price:number;
    stat:string;
    time:string;


    constructor(author, bookname, by, college, id,
         price, stat, time)
    {
        this.author = author;
        this.bookname = bookname;
        this.by = by;
        this.college = college;
        this.id = id;
        this.price = price;
        this.stat = stat;
        this.time = time;
    }
}

export class Textbooks
{
    author:string;
    bookname:string;
    by:string;
    college:string;
    description:string;
    id:number;
    picture:string;
    price:number;
    stat:string;
    time:string;


    constructor(author, bookname, by, college, description, id,
        picture, price, stat, time)
    {
        this.author = author;
        this.bookname = bookname;
        this.by = by;
        this.college = college;
        this.description = description;
        this.id = id;
        this.picture = picture;
        this.price = price;
        this.stat = stat;
        this.time = time;
    }

}

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

export class AccountResgister
{
    firstname:string;
    lastname:string;
    username:string;
    password1:string;
    password2:string;
    email:string;
    fsuid:string;


    constructor(email, firstname, fsuid, lastname, password1, password2, username)
    {
        this.email = email;
        this.firstname = firstname;
        this.fsuid = fsuid;
        this.lastname = lastname;
        this.password2 = password2;
        this.password1 = password1;
        this.username = username;
    }

}

export class Username
{
    username:string;

    constructor(username)
    {
        this.username = username;
    }
}