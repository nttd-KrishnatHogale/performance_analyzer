class SQLPlanParser:

    def parse(self, plan_df):

        if plan_df is None:

            return []

        if plan_df.empty:

            return []

        plans=[]

        for _,row in plan_df.iterrows():

            plan_text=""

            if "operation" in row:

                plan_text+=str(row["operation"])

            if "options" in row:

                plan_text+=" "+str(row["options"])

            plans.append({

                "sql_id":row.get("sql_id"),

                "plan":plan_text

            })

        return plans