import { 
  observable,
  action,
} from 'mobx';
import { getResults } from './services';

class RecordStore {
  @observable records = [];

  @observable counts = 0;

  @observable page = {};

  @action getRecords = async (query) => {
    const result = await getResults(query);
    const { data: { hits } } = result;
    if (hits.hits.length === 0) {
      return;
    }
    console.log(hits.hits);
    this.records = hits.hits;
    this.counts = hits.total; 
  };
}
export default new RecordStore();
