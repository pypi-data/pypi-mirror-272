from MoonshotAI_Api.ltv_client import LTVClient
import json
from unittest import TestCase


class TestClass(TestCase):
    def test_fetch_data(self):
        end_date = "03-20-2024"
        kpi = "ngr"
        pred_time = "180"
        start_date = "03-13-2024"
        profile = "company_name"
        default = False
        token = 'Not a real token!! HAHAHA'

        output_format = 'csv'
        # output_format = 'stream'

        ltv_client = LTVClient(profile=profile, token=token, default=default)
        try:
            data = ltv_client.fetch_data(kpi=kpi, pred_time=pred_time, start_date=start_date,
                                         end_date=end_date, output_path='ltv_result/test.csv',
                                         output_format=output_format)

            if output_format == 'stream':
                loop_stream_test(data)

        except Exception as e:
            print(f"Error getting data: {e}")


def loop_stream_test(iter_content):
    for chunk in iter_content:
        print(chunk.decode('utf-8'))

    print("hold")


if __name__ == '__main__':
    TestClass().test_fetch_data()
