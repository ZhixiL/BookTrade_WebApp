import { Textbook } from './../model';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-booklist',
  templateUrl: './booklist.component.html',
  styleUrls: ['./booklist.component.css']
})
export class BooklistComponent implements OnInit {

  constructor(private rs : RestService) { }

  textbooks : Textbook[] = [];
  ngOnInit()
  {
    this.rs.readTextbookAll()
    .subscribe
      (
        (response) => 
        {
          this.textbooks = response[0]["bookdata"];
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }

      )
  }

}
