import pandas as pd


class FeatureNormalizer:
    @staticmethod
    def normalization_base100(
            df: pd.DataFrame,
            norm_level: list,
            norm_feats: list
    ) -> pd.DataFrame:
        """
        Base 100 normalization by norm_level
        """
        for norm_feat in norm_feats:
            df['max'] = df.groupby(norm_level)[norm_feat].transform('max')
            col_norm = norm_feat #+ '_norm'
            df[col_norm] = (df[norm_feat] / df['max']) * 100
            df.drop('max', axis=1, inplace=True)
        return df
