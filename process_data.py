import logging

from sql_writer import MySQLWritter


class ProcessData:

    def __init__(self, input_time_stamp, symbol_name):
        self.input_time_stamp = input_time_stamp
        self.symbol_name = symbol_name

    def get_result_data(self):
        pass

    def add_to_cache(self):
        pass

    def update_cache(self, result):
        RedisCache().add_item(f"{self.symbol_name}-{self.input_time_stamp}", result)

    def get_output_for_each_symbol(self):
        query = f"""
    		WITH total_bids
    		AS
    		(
    		select
    			bidPrice,
    			bidQuantity,
    			row_number() over (partition by symbol order by bidprice desc, startTime asc) as bid_row_num,
    			askPrice,
    			askQuantity,
    			row_number() over (partition by symbol order by askprice, startTime asc) as ask_row_num
    		from quotes 
    		where cast('{self.input_time_stamp}' as datetime) between startTime and endTime
    		)

    		select 'Best bids', bidPrice as price, bidQuantity as quantity, bid_row_num
    		from total_bids where bid_row_num <=5
    		union all
    		select 'Best asks', askPrice, askQuantity, ask_row_num
    		from total_bids where ask_row_num <=5
    	"""
        _get_output_data(query)

    def get_output_for_symbol(self):
        query = f"""
    		WITH total_bids
    		AS
    		(
    		select
    			bidPrice,
    			bidQuantity,
    			row_number() over ( order by bidprice desc, startTime asc) as bid_row_num,
    			askPrice,
    			askQuantity,
    			row_number() over ( order by askprice, startTime asc) as ask_row_num
    		from quotes  
    		where symbol = '{self.symbol_name}' and 
    		cast('{self.input_time_stamp}' as datetime) between startTime and endTime
    		)

    		select 'Best bids', bidPrice as price, bidQuantity as quantity, bid_row_num
    		from total_bids where bid_row_num <=5
    		union all
    		select 'Best asks', askPrice, askQuantity, ask_row_num
    		from total_bids where ask_row_num <=5
    	"""
        return _get_output_data(query)

    def process(self):
        if f"{self.symbol_name}-{self.input_time_stamp}" in RedisCache().cache:
            logging.info(f"{self.symbol_name} and  {self.input_time_stamp} available in cache")
            return RedisCache().cache[f"{self.symbol_name}-{self.input_time_stamp}"]
        else:
            result = self.get_output_for_symbol()
            logging.info(result)
            self.update_cache(result)


class RedisCache:
    _instance = None
    cache = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def add_item(self, key, value):
        RedisCache.cache[key] = value

    def update_item(self, key, value):
        if key in self.cache:
            RedisCache.cache[key] = value
        else:
            raise ValueError(f"{key} does not exist in dictionary")

    def delete_item(self, key):
        if key in RedisCache.cache:
            del RedisCache.cache[key]
        else:
            raise ValueError(f"{key} does not exist in dictionary")

    def get_item(self, key):
        return RedisCache.cache.get(key, None)


def _get_output_data(input_query):
    output_list = {'Best bids': '', 'Best asks': ''}
    writter = MySQLWritter()
    # logging.info(input_query)
    results = writter.execute_and_return(input_query)
    for row in results:
        if row[0] == 'Best bids':
            output_list['Best bids'] += f" {row[1]} ({row[2]});"
        elif row[0] == 'Best asks':
            output_list['Best asks'] += f"{row[1]} ({row[2]});"
    return output_list
