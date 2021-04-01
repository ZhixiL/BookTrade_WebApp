import { Component, OnInit } from '@angular/core';
import { Textbook, Account } from './../model';
import { RestService } from '../Services/rest.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-book-detail',
  templateUrl: './book-detail.component.html',
  styleUrls: ['./book-detail.component.css']
})
export class BookDetailComponent implements OnInit {

  constructor(private rs : RestService, private route: ActivatedRoute) { }
  textbook : Textbook[] = [];
  tbook : string;
  ngOnInit()
  {
    this.rs.readTextbookAll()
      .subscribe
        (
          (response2) => 
          {
            this.textbook = response2[0]["bookdata"];
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }
        )

    this.route.paramMap
        .subscribe(params => {
          this.tbook = params.get('bookname');
          console.log(this.tbook);
        })
  }

}