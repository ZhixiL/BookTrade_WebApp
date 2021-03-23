import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
//import { RestService } from '../Services/rest.service';
import { Username, Textbook, Account } from './../model';
//import { Textbook } from './../model';
import { RestService } from './../Services/rest.service';
import {NgForm} from '@angular/forms';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})

export class PostComponent implements OnInit {
  
  constructor(private rs : RestService) { }

  textbooks : Textbook[] = [];
  constTXBK : Textbook[] = [];
  accounts : Account[] = [];
  ngOnInit()
  {
    this.rs.readTextbookAll()
    .subscribe
      (
        (response) => 
        {
          this.constTXBK = this.textbooks = response[0]["bookdata"];
                  
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }
      )
  }

  ngForm(value) {
    console.log(value);
  }

  logForm(value) {
    console.log(value);
  }

  postService (event: any) {
    this.textbooks = this.constTXBK; //repair the textbook, then filter.
  }
  
/*
  postService(event) {
    posted.preventDefault();
    const target = posted.target;
    const BookName = target.querySelector('#BookName').value;
    const Author = target.querySelector('#Author').value;
    const Price = target.querySelector('#Price').value;
    const status = target.querySelector('#status').value;
    const college = target.querySelector('#college').value;
    const file = target.querySelector('#file').value;

    var info = {
      bkname: BookName, aut: Author, post_price: Price, stat: status, coll: college, ava: file
    };
  
  constructor(private http : HttpClient) { }
  ngOnInit(){
  }
  baseUrl : string = "http://127.0.0.1:5000";
  readTextbook()
  {
    return this.http.get<Textbook[]>(this.baseUrl + "/booklistbrief");
  }

  readTextbookProfile()
  {
    return this.http.get<Textbook[]>(this.baseUrl + "/profilebook");
  }

  readTextbookAll()
  {
    return this.http.get<Textbook[]>(this.baseUrl + "/booklistall");
  }

  readUserData()
  {
    return this.http.get<Account[]>(this.baseUrl + "/profile");
  }

  readUsernameData()
  {
    return this.http.get<Username[]>(this.baseUrl + "/usernamedata");
  }

  readAccData() 
  {
    return this.http.get<Account[]>(this.baseUrl + "/login");
  }

/*
export class PostComponent implements OnInit {

  constructor(private rs : RestService){}

  headers = ["title", "author", "date", "price"]

  textbook : Textbook[] = [];

  ngOnInit()
  {
      this.rs.readTextbook()
      .subscribe
        (
          (response) => 
          {
            this.textbook = response[0]["data"];
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }

        )
  }
  
    /*console.log(info);
    // this.us.getUserAndPass(username, password);
    this.http.post('http://127.0.0.1:5000/login', JSON.stringify(info))
        .subscribe((response)=>{
      let result=response["response"];
      console.log(result);
    });
  } */

}
