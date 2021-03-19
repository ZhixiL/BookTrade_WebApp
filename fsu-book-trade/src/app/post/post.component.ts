import { Textbook } from './../Textbook';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})
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
}
