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