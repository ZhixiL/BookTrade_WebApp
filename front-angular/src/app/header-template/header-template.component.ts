import { EventEmitterService } from './../Services/event-emitter.service';
import { Router } from '@angular/router';
import { Username } from './../model';
import { RestService } from './../Services/rest.service';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-header-template',
  templateUrl: './header-template.component.html',
  styleUrls: ['./header-template.component.css']
})
export class HeaderTemplateComponent implements OnInit {

  constructor(private rs : RestService, private ees : EventEmitterService) {}
  username : string;

  ngOnInit()
  {
    this.rs.readUsernameData()
    .subscribe
      (
        (response) => 
        {
          this.username = response["username"];
        },
        (error) =>
        {
          console.log("No Data Found" + error);
        }

      )
  }

  listSearch(event)
  {
    const target = event.target;
    const key = target.querySelector('#key').value;
    this.ees.searchButtonClick(key);
  }
  
}
