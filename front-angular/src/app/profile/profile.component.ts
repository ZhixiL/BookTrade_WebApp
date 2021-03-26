import { Textbook, Account } from './../model';
import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  constructor(
    private rs : RestService, 
    private rs2 : RestService,
    private http : HttpClient,
    private route: ActivatedRoute) {}

  headers = ["avatar", "email", "firstname", "fsuid", "lastname", 
              "num_of_posts", "password", "username"]
  user : Account[] = [];
  textbook : Textbook[] = [];
  textbook2 : Textbook[] = [];
  usern : string;
  returnMsg: string;
  ngOnInit()
  {

    this.route.paramMap
    .subscribe(params => {
      this.usern = params.get('user');
      console.log(this.usern);
    })

      this.rs.readUserDataAll()
      .subscribe
        (
          (response) => 
          {
            this.user = response[0]["userdata"];
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }

        )

       this.rs.readTextbookAll()
      .subscribe
        (
          (response2) => 
          {
            this.textbook = response2[0]["bookdata"];
            var j;
            j = 0;
            for (var tb of this.textbook)
            {
              if (tb.by==this.usern && j<8)
              {
                j = j+1;
                (this.textbook2).push(tb);
                console.log(tb);
              }
            }
            j = 0;
          },
          (error) =>
          {
            console.log("No Data Found" + error);
          }
        )
        
  }

}
