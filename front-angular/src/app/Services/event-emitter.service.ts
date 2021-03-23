import { Injectable, EventEmitter } from '@angular/core';
import { Subscription } from 'rxjs/internal/Subscription';

@Injectable({
  providedIn: 'root'
})
export class EventEmitterService {
  invokeSearch = new EventEmitter();    
  subsVar: Subscription;    
    
  constructor() { }    
    
  searchButtonClick() {    
    this.invokeSearch.emit();    
  }    
}