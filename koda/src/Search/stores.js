import { 
  observable,
} from 'mobx';
import { getResults } from './services';

class Record {
  @observable records = [];

  @action getRecords = (query) {
    let result = await getResults(query);
  };
}