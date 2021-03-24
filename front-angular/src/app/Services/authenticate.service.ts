import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthenticateService {

  private BASE_URL: string = 'http://localhost:5000/authenticate';
  private headers: Headers = new Headers({'Content-Type': 'application/json'});
  constructor(private http: HttpClient) {}

}
