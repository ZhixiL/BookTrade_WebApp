import { HttpClient, JsonpClientBackend } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import 'rxjs/Rx';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.css']
})
export class PostComponent implements OnInit {

  readonly BASE_URL = 'http://localhost:5000/ping'
  constructor( private http: HttpClient) { }

  post: any;

  getPosts() {
    var temp = this.http.get(this.BASE_URL)
    this.post = this.http.get(this.BASE_URL).map(r: string => response.json())
  }

  ngOnInit(): void {
  }
}
