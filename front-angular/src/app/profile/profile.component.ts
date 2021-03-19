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

  constructor(private rs : RestService) { }

  headers = ["avatar", "email", "firstname", "fsuid", "lastname", 
              "num_of_posts", "password", "username"]
  users : Account[] = [];

  ngOnInit()
  {
    
  }

}
