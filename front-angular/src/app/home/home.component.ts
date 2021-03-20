import { Textbook } from './../model';
import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private rs : RestService){}

  headers = ["author", "bookname", "by", "college", "description",
              "id", "picture", "price", "stat", "time"]

  textbook : Textbook[] = [];

  ngOnInit()
  {
      this.rs.readTextbook()
      .subscribe
        (
          (response) => 
          {
            this.textbook = response[0]["bookdata"];
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }

        )
  }

}
