import { Injectable, EventEmitter } from '@angular/core';
import { Subscription } from 'rxjs/internal/Subscription';

@Injectable({
  providedIn: 'root'
})
export class EventEmitterService {
  invokeSearch = new EventEmitter(); 
  invokeHeaderRefresh = new EventEmitter();   
  searchSubsVar: Subscription;
  refreshSubVar: Subscription;
  key:string;
  constructor() { }    
    
  searchButtonClick(key) {  
    this.key = key; 
    this.invokeSearch.emit();    
  }

  refreshName(){
    this.invokeHeaderRefresh.emit();
  }
}