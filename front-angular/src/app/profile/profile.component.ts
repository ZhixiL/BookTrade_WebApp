import { Textbook } from './../Textbook';
import { Component, OnInit } from '@angular/core';
import { RestService } from '../Services/rest.service';
import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Account } from '../Account';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  constructor(private rs : RestService) {}

  headers = ["avatar", "email", "firstname", "fsuid", "lastname", 
              "num_of_posts", "password", "username"]
  user : Account[] = [];
  textbook : Textbook[] = [];

  ngOnInit()
  {
      this.rs.readUserData()
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

      // this.rs2.readTextbook()
      // .subscribe
      //   (
      //     (response2) => 
      //     {
      //       this.textbook = response2[0]["bookdata"];
      //     },
      //     (error) =>
      //     {
      //       console.log("No Data Found" + error);
      //     }

      //   )
  }

}
